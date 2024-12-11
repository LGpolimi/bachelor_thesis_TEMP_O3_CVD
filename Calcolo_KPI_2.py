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

# Selezionare le colonne richieste per l'output e creare una copia esplicita
output_df = merged_df[[
    'percentile_AREU', 'percentile_CAMS', 'ID_zona', 'anno', 'ritardo_giorni', 'KPI'
]].copy()  # .copy() per evitare il SettingWithCopyWarning

# Rimuovere i decimali per tutte le colonne tranne la colonna 'KPI'
output_df['percentile_AREU'] = output_df['percentile_AREU'].astype(int)
output_df['percentile_CAMS'] = output_df['percentile_CAMS'].astype(int)
output_df['ID_zona'] = output_df['ID_zona'].astype(int)
output_df['anno'] = output_df['anno'].astype(int)
output_df['ritardo_giorni'] = output_df['ritardo_giorni'].astype(int)

# Non fare alcuna formattazione per la colonna 'KPI', per mantenere tutte le cifre decimali
# La colonna 'KPI' mantiene il formato nativo
output_df['KPI'] = output_df['KPI'].astype(str)  # Assicurati che KPI sia in formato stringa per la concatenazione

# Concatenare i valori di ogni riga in un'unica stringa separata da virgole
output_df['output_string'] = output_df.apply(lambda row: ','.join(row.astype(str)), axis=1)

# Prima di salvare, aggiungere manualmente i nomi delle colonne
columns_header = 'percentile_AREU,percentile_CAMS,ID_zona,anno,ritardo_giorni,KPI'

# Scrivere i dati nel file CSV con header
output_df[['output_string']].to_csv(output_path, mode='w', index=False, header=False)

# Scrivere prima la riga di intestazione e poi i dati
with open(output_path, 'r') as f:
    data = f.readlines()

# Scrivere prima la riga di intestazione e poi i dati
with open(output_path, 'w') as f:
    f.write(columns_header + '\n')  # Scrive i nomi delle colonne
    f.writelines(data)

print(f"Calcolo KPI completato. Output salvato in: {output_path}")
