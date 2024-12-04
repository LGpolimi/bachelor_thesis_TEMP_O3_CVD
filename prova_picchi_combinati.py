'''
iniziamo a calcolare i picchi combinati
    - picchi AREU calcolati al 95esimo percentile
    - picchi CAMS calcolati dal 90esimo al 99esimo percentile con incremento di 1

iniziamo con un confronto tra i picchi con delay=0
procederemo poi a gestire i vari delay

ripetiamo l'operazione per i picchi calcolati per ogni percentile
'''

import os
import pandas as pd

# Percorsi di input dei dati
input_AREU = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\picchi_AREU_95perc.csv"
input_CAMS = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\picchi_CAMS.csv"

# Percorso output per il salvataggio dei dati
output_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\prova_picchi"
output_file = os.path.join(output_path, "picchi_combinati.csv")
summary_file = os.path.join(output_path, "numero_picchi_per_percentile.csv")

# Caricamento dei dataset
areu_df = pd.read_csv(input_AREU)
cams_df = pd.read_csv(input_CAMS)

# Creare una lista per raccogliere i risultati
results = []
summary = []

# Ciclo attraverso i percentili dal 90 al 99
for percentile in range(90, 100):
    # Filtrare il dataset CAMS per il percentile corrente
    cams_filtered = cams_df[cams_df["percentile"] == percentile]

    # Effettuare il merge con i dati AREU sulla data e griglia geografica
    combined_df = pd.merge(
        cams_filtered, areu_df,
        left_on=["time", "LMB3A_IDcu"],
        right_on=["DATA", "id_cella"],
        how="inner"
    )

    # Aggiungere il valore del percentile come colonna
    combined_df["percentile"] = percentile

    # Aggiungere il risultato corrente alla lista
    results.append(combined_df)

    # Salvare il numero totale di picchi per questo percentile
    summary.append({"percentile": percentile, "numero_picchi": len(combined_df)})

# Concatenare tutti i risultati in un unico DataFrame
final_df = pd.concat(results, ignore_index=True)

# Creare un DataFrame per il riassunto
summary_df = pd.DataFrame(summary)

# Selezionare solo le colonne necessarie
final_df = final_df[["time", "LMB3A_IDcu", "ozono", "temperatura", "casi", "percentile"]]
final_df.rename(columns={"time": "data", "LMB3A_IDcu": "zona_geografica"}, inplace=True)

# Creare la directory di output se non esiste
os.makedirs(output_path, exist_ok=True)

# Salvare il risultato in un file CSV
final_df.to_csv(output_file, index=False)

# Salvare il riassunto in un file CSV
summary_df.to_csv(summary_file, index=False)

print(f"File dei picchi combinati salvato in: {output_file}")
print(f"Riassunto del numero di picchi per percentile salvato in: {summary_file}")


