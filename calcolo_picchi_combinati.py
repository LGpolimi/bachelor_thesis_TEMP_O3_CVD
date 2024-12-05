'''
iniziamo a calcolare i picchi combinati
    - picchi AREU calcolati dal 90esimo al 99esimo percentile con incremento di 1
    - picchi CAMS calcolati dal 90esimo al 99esimo percentile con incremento di 1

iniziamo con un confronto tra i picchi con delay=0
procederemo poi a gestire i vari delay

ripetiamo l'operazione per i picchi calcolati per ogni percentile
'''

import os
import pandas as pd

# Percorsi di input dei dati
input_AREU = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi"
input_CAMS = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\picchi_CAMS.csv"

# Percorso output per il salvataggio dei dati
output_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\picchi_combinati"
os.makedirs(output_path, exist_ok=True)  # Creare la directory di output se non esiste

# Carico il dataset CAMS
cams_df = pd.read_csv(input_CAMS)

# DataFrame per contenere tutti i dati combinati
all_combinations_df = pd.DataFrame()

# Lista per il riepilogo delle combinazioni
summary_combinations = []

# Ciclo attraverso i percentili dal 90 al 99
for percentile_areu in range(90, 100):
    areu_file = os.path.join(input_AREU, f"Picchi_AREU({percentile_areu}°percentile).csv")

    if not os.path.exists(areu_file):
        print(f"File non trovato: {areu_file}. Saltando questo percentile.")
        continue

    # Carico i dati AREU per il percentile corrente
    areu_df = pd.read_csv(areu_file)

    # Ciclo attraverso i percentili CAMS
    for percentile_cams in range(90, 100):
        # Filtrare il dataset CAMS per il percentile corrente
        cams_filtered = cams_df[cams_df["percentile"] == percentile_cams]

        # Effettuare il merge con i dati AREU sulla data e griglia geografica
        combined_df = pd.merge(
            cams_filtered, areu_df,
            left_on=["time", "LMB3A_IDcu"],
            right_on=["DATA", "id_cella"],
            how="inner"
        )

        # Aggiungere i dati della combinazione al DataFrame cumulativo
        combined_df["percentile_AREU"] = percentile_areu
        combined_df["percentile_CAMS"] = percentile_cams

        # Selezionare e rinominare le colonne per il file di output unico
        combined_df = combined_df[[
            "percentile_AREU", "percentile_CAMS",
            "time", "LMB3A_IDcu", "ozono", "temperatura", "casi"
        ]]
        combined_df.rename(
            columns={
                "time": "data",
                "LMB3A_IDcu": "zona_geografica",
                "ozono": "dato_ozono",
                "temperatura": "dato_temperatura",
                "casi": "numero_casi"
            },
            inplace=True
        )

        all_combinations_df = pd.concat([all_combinations_df, combined_df], ignore_index=True)

        #aggiungere al riepilogo il numero di picchi per questa combinazione
        summary_combinations.append({
            "percentile_AREU": percentile_areu,
            "percentile_CAMS": percentile_cams,
            "numero_picchi": len(combined_df)
        })

#salvo il DataFrame cumulativo in un unico file
output_file = os.path.join(output_path, "Combinazioni_AREU_CAMS.csv")
all_combinations_df.to_csv(output_file, index=False)

print(f"Tutte le combinazioni salvate in un unico file: {output_file}")

#creare un DataFrame per il riepilogo delle combinazioni
summary_df = pd.DataFrame(summary_combinations)

#salvo il file di riepilogo
summary_file = os.path.join(output_path, "Riepilogo_combinazioni_percentili.csv")
summary_df.to_csv(summary_file, index=False)

print(f"Riepilogo delle combinazioni di percentili salvato in: {summary_file}")

