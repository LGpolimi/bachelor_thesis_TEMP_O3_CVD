'''
calcolo dei KPI - questi verranno calcolati nel seguente modo:
    - zona per zona
    - percentile per percentile
    - a denominatore del calcolo dei kpi si tiene la somma di tutti i casi dal 2015 al 2019
'''

import pandas as pd

# Percorsi di input
input_CAMS = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\totale_picchi_CAMS_per_zona.csv"
input_picchi_combinati = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\totale_picchi_combinati_per_zona.csv"

# Percorso di output
output_CAMS = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\KPI_2015_2019"

# Caricamento dei dati
df_CAMS = pd.read_csv(input_CAMS)
df_picchi_combinati = pd.read_csv(input_picchi_combinati)

# Rinominare le colonne del dataset CAMS come da tua richiesta
df_CAMS = df_CAMS.rename(columns={'percentile_CAMS': 'perc_CAMS', 'zona_geografica': 'ID_zona'})

# Verifica i nomi delle colonne
print("Colonne di df_CAMS:", df_CAMS.columns)
print("Colonne di df_picchi_combinati:", df_picchi_combinati.columns)

# Unire i due dataframe sui campi 'ID_zona' e 'perc_CAMS'
df = pd.merge(df_CAMS, df_picchi_combinati, left_on=['ID_zona', 'perc_CAMS'],
              right_on=['zona_geografica', 'percentile_CAMS'])

# Stampa le prime righe del dataframe risultante
print(df.head())

# Verifica il numero di righe dopo il merge
print(f"Numero di righe dopo il merge: {len(df)}")

# Verifica il numero di zone geografiche uniche
totale_zone_geografiche = len(df['ID_zona'].unique())
print(f"Totale zone geografiche nel dataset: {totale_zone_geografiche}")

# Creazione delle combinazioni di delay da 0 a 4 giorni
delay_range = list(range(0, 5))

# Creazione di un dataframe vuoto per raccogliere i risultati
result = []

# Calcolo del KPI per ogni combinazione di percentili, zone geografiche e delay
for perc_CAMS in df['perc_CAMS'].unique():  # Iterare sui percentili CAMS
    for perc_AREU in df['percentile_AREU'].unique():  # Iterare sui percentili AREU
        for delay in delay_range:  # Iterare sui delay (0-4)
            for zona in df['ID_zona'].unique():  # Iterare su tutte le zone geografiche
                # Filtriamo il dataframe per la combinazione corrente di percentile CAMS, AREU, delay e zona
                df_filtered = df[(df['perc_CAMS'] == perc_CAMS) &
                                 (df['percentile_AREU'] == perc_AREU) &
                                 (df['delay'] == delay) &
                                 (df['ID_zona'] == zona)]

                # Calcolare il KPI come (totale picchi combinati) / (totale picchi cams)
                if not df_filtered.empty:
                    kpi = df_filtered['picchi_combinati'].sum() / df_filtered['totale_picchi_per_zona'].sum()

                    # Aggiungere il risultato alla lista
                    result.append({
                        'percentile_AREU': perc_AREU,
                        'percentile_CAMS': perc_CAMS,
                        'ID_zona': zona,
                        'delay': delay,
                        'KPI': kpi
                    })

# Creazione del dataframe finale con i risultati
df_result = pd.DataFrame(result)

# Salvataggio del risultato in un file CSV di output
df_result.to_csv(output_CAMS + r"\kpi_per_zona_completo.csv", index=False)

print(f"File KPI salvato in: {output_CAMS}\\kpi_per_zona_completo.csv")
