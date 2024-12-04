'''
calcoliamo i piacchi dei dati normalizzati e combinati CAMS
calcolati su tutte le griglie a partire dal 90esimo percentile con un incremento di 1
'''

import pandas as pd

#percorso del file di input
input_path = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_uniti_normalizzati\dati_uniti_normalizzati.csv"

#percorso del file di output
output_path_peaks = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\picchi_per_percentile.csv"
output_path_totals = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\totali_picchi_per_percentile.csv"

data = pd.read_csv(input_path)

#verifica delle colonne richieste
required_columns = ['LMB3A_IDcu', 'time', 'sum_normalized', 'temperatura', 'ozono']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"Il file deve contenere le colonne: {', '.join(required_columns)}")

#calcolo dei picchi per ciascuna griglia
results = []
percentiles = list(range(90, 100))  # Dal 90° al 99° percentile

groups = data.groupby('LMB3A_IDcu')
for grid_id, group in groups:
    for p in percentiles:
        threshold = group['sum_normalized'].quantile(p / 100)
        peaks = group[group['sum_normalized'] > threshold]
        for _, row in peaks.iterrows():
            results.append({
                'time': row['time'],
                'LMB3A_IDcu': grid_id,
                'percentile': p,
                'sum_normalized': row['sum_normalized'],
                'temperatura': row['temperatura'],
                'ozono': row['ozono']
            })

#creo il DataFrame dei picchi
peaks_df = pd.DataFrame(results)

#calcolo del totale dei picchi per percentile
totals_per_percentile = peaks_df.groupby('percentile').size().reset_index(name='total_peaks')

#salvataggio dei file
peaks_df.to_csv(output_path_peaks, index=False)  # Dati sui picchi
totals_per_percentile.to_csv(output_path_totals, index=False)  # Totali dei picchi per percentile

#print per controllo
print("File salvati con successo:")
print(f"- Dati sui picchi: {output_path_peaks}")
print(f"- Totali dei picchi per percentile: {output_path_totals}")
