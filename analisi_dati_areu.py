import pandas as pd
import xarray as xr
import glob
import os

df = pd.read_csv(r"C:\Users\bruno\OneDrive\Desktop\Dati grezzi\1. AREU\EVT_MISS_PZ_2015.tab",low_memory=False,encoding='ISO-8859-1',on_bad_lines='skip',sep='\t')
#print(df.iloc[0, 50:]) #questo comando permette di selezionare la riga in posizione 0 e tutte le colonne dalla 50 all'ultima

#visualizzo il motivo della chiamata
#print(df['MOTIVO'].head())

#motivo_chiamata=df['MOTIVO_DTL'].unique()
#print(motivo_chiamata)

#con questo ciclo for otteniamo in output le dimensioni dei dataframe AREU per ogni annata
for anno in range (2015, 2024):
    df = pd.read_csv(r"C:\Users\bruno\OneDrive\Desktop\Dati grezzi\1. AREU\EVT_MISS_PZ_" +str(anno) + ".tab", low_memory=False,
                     #encoding='ISO-8859-1', on_bad_lines='skip', sep='\t')
    print(df.shape, 'anno: ', str(anno))

#con questo ciclo for otteniamo in output le dimensioni dei dataframe AREU per ogni annata dopo la pulizia
for anno in range (2015, 2024):
    df = pd.read_csv(r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_AREU_filtrati\EVT_MISS_PZ_" +str(anno) + ".tab", low_memory=False,
                     encoding='ISO-8859-1', on_bad_lines='skip', sep='\t')
    print(df.shape, 'anno: ', str(anno))
