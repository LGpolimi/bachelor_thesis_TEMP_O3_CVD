import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

def processa_dati(input_csv, input_griglia, output_path, output_name, colonna_valore, colonna_tempo):
    """
    Processa un file CSV contenente dati georeferenziati e li unisce a una griglia geografica.
    Aggrega i dati per griglia geografica e tempo, calcolando la media giornaliera del valore specificato.

    input_csv: Percorso del file dataframe .csv contenente i dati.
    input_griglia: Percorso del file .shp della griglia geografica.
    output_path: Percorso della cartella di output per i file salvati.
    output_name: Nome base per i file di output (senza estensione).
    colonna_valore: Nome della colonna nei dati da aggregare (es. 't2m' o 'pollution').
    colonna_tempo: Nome della colonna che rappresenta il tempo (es. 'time').
    """

    # Carico i dati della griglia
    griglia = gpd.read_file(input_griglia)

    # Verifico che la griglia contenga la colonna `LMB3A_IDcu`
    if 'LMB3A_IDcu' not in griglia.columns:
        raise KeyError("La griglia caricata non contiene una colonna 'LMB3A_IDcu'. Controlla i dati della griglia.")

    # Carico il file CSV contenente i dati puntuali
    dati = pd.read_csv(input_csv)

    # Verifico che il file CSV contenga colonne 'latitude', 'longitude', e `colonna_tempo`
    if 'latitude' not in dati.columns or 'longitude' not in dati.columns:
        raise ValueError("Il CSV deve contenere colonne 'latitude' e 'longitude' per le coordinate.")
    if colonna_tempo not in dati.columns:
        raise ValueError(f"Il CSV deve contenere una colonna '{colonna_tempo}' che rappresenti il tempo.")

    # Debug: Conferma che la colonna temporale è già corretta
    print(f"Primi valori nella colonna '{colonna_tempo}':\n{dati[colonna_tempo].head()}")

    # Converto il CSV in GeoDataFrame
    geometry = [Point(xy) for xy in zip(dati['longitude'], dati['latitude'])]
    gdf_dati = gpd.GeoDataFrame(dati, geometry=geometry)

    # Imposto il sistema di riferimento (WGS84, EPSG:4326)
    gdf_dati.set_crs(epsg=4326, inplace=True)

    # Riprojietto i dati puntuali sulla griglia
    if gdf_dati.crs != griglia.crs:
        gdf_dati = gdf_dati.to_crs(griglia.crs)

    # Associo ogni punto alla cella della griglia
    dati_uniti = gpd.sjoin(griglia, gdf_dati, how="inner", predicate="intersects")

    # Verifico che l'unione spaziale abbia prodotto dati
    if dati_uniti.empty:
        raise ValueError("L'unione spaziale non ha prodotto risultati. Verifica che le geometrie e i CRS siano corretti.")

    # Controllo che `colonna_valore` sia nei dati uniti
    if colonna_valore not in dati_uniti.columns:
        raise KeyError(f"La colonna '{colonna_valore}' non è presente nei dati uniti. Controlla il CSV.")

    # Raggruppo i dati per cella geografica e giorno, calcolando la media giornaliera
    statistiche = (
        dati_uniti.groupby(["LMB3A_IDcu", colonna_tempo])[colonna_valore]
        .mean()
        .reset_index()
        .rename(columns={colonna_valore: "mean_value"})
    )

    # Debug: Controlla i risultati del raggruppamento
    print(f"Primi risultati raggruppati:\n{statistiche.head()}")

    # Calcolo latitudine e longitudine medie per ciascuna cella geografica
    coordinate_medie = (
        dati_uniti.groupby("LMB3A_IDcu")[["latitude", "longitude"]]
        .mean()
        .reset_index()
    )

    # Unisco le coordinate medie ai risultati aggregati
    risultati = statistiche.merge(coordinate_medie, on="LMB3A_IDcu", how="left")

    # Salvo i risultati come CSV, shapefile e GeoJSON
    output_csv = os.path.join(output_path, f"{output_name}.csv")
    output_shp = os.path.join(output_path, f"{output_name}.shp")
    output_geojson = os.path.join(output_path, f"{output_name}.geojson")

    # Salvataggio CSV
    risultati.to_csv(output_csv, index=False)

    # Convertiamo risultati in GeoDataFrame per salvataggio shapefile e GeoJSON
    risultati_gdf = griglia.merge(risultati, on="LMB3A_IDcu", how="left")
    risultati_gdf.to_file(output_shp)
    risultati_gdf.to_file(output_geojson, driver="GeoJSON")

    print(f"Elaborazione completata per {output_name}. File salvati in:\n- {output_csv}\n- {output_shp}\n- {output_geojson}")


# Percorsi cartelle/file CSV
input_temperature = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_definitivi\dati_CAMS_temperatura.csv"
input_ozono = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_definitivi\dati_CAMS_ozono.csv"
input_griglia = r"C:\Users\bruno\OneDrive\Desktop\Dati grezzi\4. GriglieGeografiche\LMB3A.shp"
output_path = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_griglie"

# Elaborazione per temperatura (colonna 't2m')
processa_dati(input_temperature, input_griglia, output_path, "output_temperatura", colonna_valore="t2m", colonna_tempo="time")

# Elaborazione per ozono (colonna 'pollution')
processa_dati(input_ozono, input_griglia, output_path, "output_ozono", colonna_valore="pollution", colonna_tempo="time")
