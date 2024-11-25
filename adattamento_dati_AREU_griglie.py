import pandas as pd
import geopandas as gpd
import os

#percorsi dei dati in input e output
input_dati = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_elaborati\\dati_definitivi\\dati_AREU.csv"
input_griglia = r"C:\\Users\\bruno\\OneDrive\\Desktop\\Dati grezzi\\4. GriglieGeografiche\\LMB3A.shp"
output_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_elaborati\\dati_adattati_griglie"

#Leggo il dataset AREU
data = pd.read_csv(input_dati)

#convertire la colonna DATA in formato datetime
if 'DATA' in data.columns:
    data['DATA'] = pd.to_datetime(data['DATA'], errors='coerce')  # Converte e gestisce eventuali errori
else:
    raise ValueError("La colonna 'DATA' non è presente nel dataset.")

#verifico se ci sono valori non convertiti (NaT)
if data['DATA'].isnull().sum() > 0:
    print("Attenzione: alcuni valori in 'DATA' non sono validi datetime e saranno ignorati.")

#creo un GeoDataFrame da LAT e LONG
if 'LAT' not in data.columns or 'LONG' not in data.columns:
    raise ValueError("Il dataset deve contenere le colonne 'LAT' e 'LONG'.")

#creo geometrie dai campi LAT e LONG
data_gdf = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(data['LONG'], data['LAT']),
    crs="EPSG:4326"  # Sistema di riferimento spaziale WGS84
)

#leggo la griglia geografica
grids = gpd.read_file(input_griglia)

if grids.crs != data_gdf.crs:
    grids = grids.to_crs(data_gdf.crs)

#aggiungo un identificativo univoco alla griglia (se non presente)
if 'id_cella' not in grids.columns:
    grids['id_cella'] = grids.index

#Unisco i dati con la griglia
#associa ogni punto a una cella della griglia utilizzando un spatial join
data_with_grid = gpd.sjoin(data_gdf, grids, how="left", predicate="intersects")

#aggiungo una colonna per contare i casi
data_with_grid['casi'] = 1

#sommo i casi totali per giorno e cella
result = (
    data_with_grid.groupby(['DATA', 'id_cella'])
    .agg({
        'casi': 'sum'  # Somma i casi
    })
    .reset_index()
)

#unisco il risultato con la geometria della griglia per ottenere geometrie per cella
result = result.merge(grids[['id_cella', 'geometry']], on='id_cella', how='left')

result_gdf = gpd.GeoDataFrame(result, geometry='geometry', crs=grids.crs)

#forzo la colonna 'DATA' nel formato 'date' per shapefile
#la conversione a 'date' (senza l'ora) per evitare l'avviso
result_gdf['DATA'] = result_gdf['DATA'].dt.date  # Converte a solo data (senza ora)

#salvo l'output come shapefile
output_shapefile = os.path.join(output_path, "dati_AREU_griglie.shp")
result_gdf.to_file(output_shapefile)
print(f"File shapefile salvato con successo in {output_shapefile}")

#salvo anche come CSV
output_csv = os.path.join(output_path, "dati_AREU_griglie.csv")
result_gdf.drop(columns='geometry').to_csv(output_csv, index=False)
print(f"File CSV salvato con successo in {output_csv}")
