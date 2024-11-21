import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os


def processa_dati(input_csv, input_griglia, output_path, output_name, colonna_valore):

    """
    Processa un file CSV contenente dati georeferenziati e li unisce a una griglia geografica.
    Salva i risultati come shapefile e GeoJSON.

    input_csv: Percorso del file dataframe .csv contenente i dati
    input_griglia: Percorso del file .shp della griglia geografica.
    output_path: Percorso della cartella di output per i file salvati.
    output_name: Nome base per i file di output (senza estensione).
    colonna_valore: Nome della colonna nei dati da aggregare (es. 't2m' per temperatura, 'pollution' per ozono).
    """

    #Carico i dati
    griglia = gpd.read_file(input_griglia)

    #verifico che la griglia contenga la colonna `LMB3A_IDcu`
    #LMB3A_IDcu è la griglia con la suddivisione in zone per 100mila abitanti
    if 'LMB3A_IDcu' not in griglia.columns:
        raise KeyError("La griglia caricata non contiene una colonna 'LMB3A_IDcu'. Controlla i dati della griglia.")

    #carico il file CSV contenente i dati puntuali
    dati = pd.read_csv(input_csv)

    #verifico che il file CSV contenga colonne 'latitude' e 'longitude'
    if 'latitude' not in dati.columns or 'longitude' not in dati.columns:
        raise ValueError(f"Il CSV {input_csv} deve contenere colonne 'lat' e 'lon' per le coordinate.")

    #converto il CSV in GeoDataFrame
    #creo le geometrie dalle colonne latitude e longitude
    geometry = [Point(xy) for xy in zip(dati['longitude'], dati['latitude'])]
    gdf_dati = gpd.GeoDataFrame(dati, geometry=geometry)

    #imposto il sistema di riferimento (WGS84, EPSG:4326)
    gdf_dati.set_crs(epsg=4326, inplace=True)

    #riproglietto i dati puntuali sulla griglia
    if gdf_dati.crs != griglia.crs:
        gdf_dati = gdf_dati.to_crs(griglia.crs)

    #associo ogni punto alla cella della griglia
    dati_uniti = gpd.sjoin(griglia, gdf_dati, how="inner", predicate="intersects")

    #verifica che l'unione spaziale abbia prodotto dati
    if dati_uniti.empty:
        raise ValueError(
            "L'unione spaziale non ha prodotto risultati. Verifica che le geometrie e i CRS siano corretti.")

    #controllo quali colonne sono presenti dopo l'unione
    print(f"Colonne presenti dopo l'unione spaziale: {dati_uniti.columns.tolist()}")

    #calcolo la media del valore per ogni cella geografica
    if colonna_valore not in dati_uniti.columns:
        raise KeyError(
            f"La colonna '{colonna_valore}' non è presente nei dati uniti. Assicurati che il CSV contenga una colonna con i dati da aggregare.")

    statistiche = dati_uniti.groupby("LMB3A_IDcu")[colonna_valore].mean().reset_index()

    #unisco le statistiche calcolate alla griglia
    griglia = griglia.merge(statistiche, on="LMB3A_IDcu", how="left")

    #salvo i file nella cartella di output
    output_shp = os.path.join(output_path, f"{output_name}.shp")
    output_geojson = os.path.join(output_path, f"{output_name}.geojson")

    griglia.to_file(output_shp)
    griglia.to_file(output_geojson, driver="GeoJSON")

    print(f"Elaborazione completata per {output_name}. File salvati in:\n- {output_shp}\n- {output_geojson}")


#percorsi cartelle/file CSV
input_temperature = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_definitivi\dati_CAMS_temperatura.csv"
input_ozono = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_definitivi\dati_CAMS_ozono.csv"
input_griglia = r"C:\Users\bruno\OneDrive\Desktop\Dati grezzi\4. GriglieGeografiche\LMB3A.shp"
output_path = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_griglie"

#elaborazione per temperatura (colonna 't2m')
processa_dati(input_temperature, input_griglia, output_path, "output_temperatura", colonna_valore="t2m")

#elaborazione per ozono (colonna 'pollution')
processa_dati(input_ozono, input_griglia, output_path, "output_ozono", colonna_valore="pollution")