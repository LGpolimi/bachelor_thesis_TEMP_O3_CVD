'''
iniziamo a calcolare i picchi combinati
    - picchi AREU calcolati dal 90esimo al 99esimo percentile con incremento di 1
    - picchi CAMS calcolati dal 90esimo al 99esimo percentile con incremento di 1

si tiene conto di un delay che va da 0 a 4 giorni
ripetiamo l'operazione per i picchi calcolati per ogni percentile

salvo un file per ogni giorno di delay, con tutte le informazioni necessarie
'''

import os
import pandas as pd
from datetime import timedelta

# Percorsi di input dei dati
input_AREU = r"C:\Users\bruno\OneDrive\Desktop\dati_calcolo_picchi\picchi_cams_areu_separati"
input_CAMS = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\5. calcolo_picchi_CAMS\picchi_per_percentile.csv"

# Percorso output per il salvataggio dei dati
output_path = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\6. picchi COMBINATI"
os.makedirs(output_path, exist_ok=True)  # Creare la directory di output se non esiste

# Carico il dataset CAMS
cams_df = pd.read_csv(input_CAMS)
cams_df["time"] = pd.to_datetime(cams_df["time"])  # Assicurarsi che il campo 'time' sia in formato datetime

# DataFrame per contenere tutti i dati combinati
all_combinations_df = pd.DataFrame()

# Ciclo attraverso i percentili dal 90 al 99
for percentile_areu in range(90, 100):
    areu_file = os.path.join(input_AREU, f"Picchi_AREU({percentile_areu}°percentile).csv")

    if not os.path.exists(areu_file):
        print(f"File non trovato: {areu_file}. Saltando questo percentile.")
        continue

    # Carico i dati AREU per il percentile corrente
    areu_df = pd.read_csv(areu_file)
    areu_df["DATA"] = pd.to_datetime(areu_df["DATA"])  # Assicurarsi che il campo 'DATA' sia in formato datetime

    # Ciclo attraverso i percentili CAMS
    for percentile_cams in range(90, 100):
        # Filtrare il dataset CAMS per il percentile corrente
        cams_filtered = cams_df[cams_df["percentile"] == percentile_cams]

        # Ciclo attraverso i ritardi (delay) da 0 a 4 giorni
        for delay in range(0, 5):
            # Modifica della data del picco AREU per considerare il delay
            areu_df["DATA_delay"] = areu_df["DATA"] - timedelta(days=delay)

            # Effettuare il merge con i dati CAMS sulla griglia geografica e sulla data modificata
            combined_df = pd.merge(
                cams_filtered, areu_df,
                left_on=["time", "LMB3A_IDcu"],
                right_on=["DATA_delay", "id_cella"],
                how="inner",
                suffixes=("_CAMS", "_AREU")
            )

            # Aggiungere i dati della combinazione al DataFrame cumulativo
            combined_df["percentile_AREU"] = percentile_areu
            combined_df["percentile_CAMS"] = percentile_cams
            combined_df["ritardo_giorni"] = delay  # Aggiungere la colonna del delay

            # Selezionare e rinominare le colonne per il file di output unico
            combined_df = combined_df[[
                "percentile_AREU", "percentile_CAMS",
                "time", "DATA", "LMB3A_IDcu", "ozono", "temperatura", "casi", "ritardo_giorni"
            ]]
            combined_df.rename(
                columns={
                    "time": "data_CAMS",
                    "DATA": "data_AREU",
                    "LMB3A_IDcu": "zona_geografica",
                    "ozono": "dato_ozono",
                    "temperatura": "dato_temperatura",
                    "casi": "numero_casi"
                },
                inplace=True
            )

            # Salvo il DataFrame per il delay corrente
            delay_output_file = os.path.join(output_path, f"Combinazioni_AREU_CAMS_delay_{delay}.csv")
            combined_df.to_csv(delay_output_file, index=False)

            print(f"File combinato salvato per il delay {delay}: {delay_output_file}")

            # Riepilogo per questa combinazione
            summary_combinations = [{
                "percentile_AREU": percentile_areu,
                "percentile_CAMS": percentile_cams,
                "ritardo_giorni": delay,
                "numero_picchi": len(combined_df)
            }]
            summary_df = pd.DataFrame(summary_combinations)

            # Salvo il riepilogo per il delay corrente
            summary_output_file = os.path.join(output_path, f"Riepilogo_combinazioni_percentili_delay_{delay}.csv")
            summary_df.to_csv(summary_output_file, index=False)

            print(f"Riepilogo salvato per il delay {delay}: {summary_output_file}")
