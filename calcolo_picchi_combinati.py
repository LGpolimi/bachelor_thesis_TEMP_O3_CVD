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

#percorsi di input dei dati
input_AREU = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi"
input_CAMS = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\picchi_CAMS.csv"

#percorso output per il salvataggio dei dati
output_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_calcolo_picchi\\picchi_combinati"
os.makedirs(output_path, exist_ok=True)  # Creare la directory di output se non esiste

#carico il dataset CAMS
cams_df = pd.read_csv(input_CAMS)

summary_combinations = []

#ciclo attraverso i percentili dal 90 al 99
for percentile_areu in range(90, 100):
    areu_file = os.path.join(input_AREU, f"Picchi_AREU({percentile_areu}°percentile).csv")

    if not os.path.exists(areu_file):
        print(f"File non trovato: {areu_file}. Saltando questo percentile.")
        continue

    #carico i dati AREU per il percentile corrente
    areu_df = pd.read_csv(areu_file)

    #ciclo attraverso i percentili CAMS
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

        #aggiungo i dati della combinazione al riepilogo
        summary_combinations.append({
            "percentile_AREU": percentile_areu,
            "percentile_CAMS": percentile_cams,
            "numero_picchi": len(combined_df)
        })

        #seleziono le colonne necessarie per l'output dettagliato
        combined_df = combined_df[["time", "LMB3A_IDcu", "ozono", "temperatura", "casi"]]
        combined_df.rename(
            columns={"time": "data", "LMB3A_IDcu": "zona_geografica"},
            inplace=True
        )

        #nome del file di output per il percentile corrente
        output_file = os.path.join(
            output_path, f"Confronto_AREU_{percentile_areu}_CAMS_{percentile_cams}.csv"
        )

        combined_df.to_csv(output_file, index=False)

        print(
            f"File di confronto per AREU {percentile_areu}° e CAMS {percentile_cams}° percentile salvato in: {output_file}")

#creo un DataFrame per il riepilogo delle combinazioni
summary_df = pd.DataFrame(summary_combinations)

summary_file = os.path.join(output_path, "Riepilogo_combinazioni_percentili.csv")

summary_df.to_csv(summary_file, index=False)

print(f"Riepilogo delle combinazioni di percentili salvato in: {summary_file}")
