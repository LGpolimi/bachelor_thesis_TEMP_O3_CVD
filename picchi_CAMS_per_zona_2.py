import pandas as pd

# Percorso del file di input
input_path = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_uniti_normalizzati\dati_uniti_normalizzati.csv"

# Percorso del file di output
output_path_summary = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_kpi\riepilogo_picchi_per_percentile_zona_anno.csv"  # Modifica percorso per includere l'anno

# Caricamento del DataFrame
data = pd.read_csv(input_path)

# Verifica colonne richieste
required_columns = ['LMB3A_IDcu', 'time', 'sum_normalized']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"Il file deve contenere le colonne: {', '.join(required_columns)}")

# Convertire la colonna 'time' in formato datetime per estrarre l'anno
data['time'] = pd.to_datetime(data['time'], errors='coerce')
data['year'] = data['time'].dt.year  # Estrai l'anno

# Filtra i dati per gli anni dal 2015 al 2019
data = data[data['year'].between(2015, 2019)]

# Calcolo dei picchi per ciascuna griglia
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
                'year': row['year']  # Aggiungi l'anno
            })

# Creazione del DataFrame dei picchi
peaks_df = pd.DataFrame(results)

# Calcolo del riepilogo per percentile, zona geografica e anno
summary_per_zone_year = peaks_df.groupby(['percentile', 'LMB3A_IDcu', 'year']).size().reset_index(name='total_peaks_per_zone')

# Salvataggio del file riepilogo
summary_per_zone_year.to_csv(output_path_summary, index=False)  # Salva solo il sommario con l'anno

# Stampa per controllo
print("File salvato con successo:")
print(f"- Riepilogo picchi per percentile, zona e anno: {output_path_summary}")
