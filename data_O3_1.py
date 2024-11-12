#NOTA: ho installato nuove librerie
#globe: per individuare i file nella cartella
#xarray: per leggere i file con estensione .nc
#libreria per permettere a xarray di leggere i file .nc. "pip install h5netcdf" nel terminale.

import xarray as xr
import pandas as pd
import glob
import os

#cartella con i dati su ozono
cartella = r"C:\Users\bruno\OneDrive\Desktop\Dati_PyCharm\CAMS"

#file con estensione .nc nella cartella
file_dati = glob.glob(cartella + "\\*.nc")

#creo una lista per accumulare i dati che vengono letti
dataframes = []

#Leggi ciascun file .nc e convertilo in DataFrame, poi aggiungilo alla lista
for file in file_dati:
    try:
        # Apri il file .nc con xarray
        ds = xr.open_dataset(file)

        # Converti il dataset xarray in un DataFrame
        df = ds.to_dataframe().reset_index()

        # Aggiungi il DataFrame alla lista
        dataframes.append(df)
    except Exception as e:
        print(f"Errore nella lettura del file {file}: {e}")

#Unisco tutti i DataFrame in un unico DataFrame
df_unito = pd.concat(dataframes, ignore_index=True)
print(df_unito)

# Salva il DataFrame pulito in un file CSV
df_unito.to_csv(r"C:\Users\bruno\OneDrive\Desktop\Dati_PyCharm\CAMS\output_dati_ozono.csv", index=False)
