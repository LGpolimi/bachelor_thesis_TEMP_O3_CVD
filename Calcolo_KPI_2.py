'''
calcolo dei KPI seguendo la formula del file precedente
calcolo che viene ripetuto per ogni anno dal 2015 al 2019
a denominatore si mettono il totale dei picchi CAMS anno per anno
'''

import pandas as pd

# Percorsi dei file
input_CAMS = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\KPI_anno_per_anno\totale_picchi_CAMS_per_zona.csv"
input_picchi_combinati = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\KPI_anno_per_anno\somma_picchi_anno_per_anno.csv"
output_path = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\KPI_anno_per_anno\KPI_output.csv"

# Caricare i dataset
cams_df = pd.read_csv(input_CAMS)
picchi_df = pd.read_csv(input_picchi_combinati)

# Rinominare colonne per uniformità se necessario (es. per facilitare il merge)
cams_df.rename(columns={
    'percentile': 'percentile_CAMS',
    'LMB3A_IDcu': 'ID_zona',
    'year': 'anno',
    'total_peaks_per_zone': 'totale_picchi_CAMS'
}, inplace=True)

picchi_df.rename(columns={
    'zona_geografica': 'ID_zona'
}, inplace=True)

# Effettuare un merge tra i due dataset
merged_df = pd.merge(picchi_df, cams_df,
                     left_on=['percentile_CAMS', 'ID_zona', 'anno'],
                     right_on=['percentile_CAMS', 'ID_zona', 'anno'],
                     how='inner')

# Calcolo del KPI
merged_df['KPI'] = merged_df['somma_picchi'] / merged_df['totale_picchi_CAMS']

# Selezionare le colonne richieste per l'output
output_df = merged_df[[
    'percentile_AREU', 'percentile_CAMS', 'ID_zona', 'anno', 'ritardo_giorni', 'KPI'
]]

# Salvare il risultato in un nuovo file CSV
output_df.to_csv(output_path, index=False, sep=';')

print(f"Calcolo KPI completato. Output salvato in: {output_path}")



