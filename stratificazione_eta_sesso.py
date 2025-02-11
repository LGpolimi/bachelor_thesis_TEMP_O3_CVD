'''
codice per suddividere i casi sanitari in base a sesso ed età
'''

import pandas as pd

# Percorsi dei file di input e output
input_1 = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\9. Dati utili scrittura tesi\picchi_AREU_eta_sesso.csv"
input_2 = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\6. Picchi COMBINATI\Combinazioni_modificate.csv"
output_path = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\9. Dati utili scrittura tesi\output_risultati.csv"

# Caricamento dei dataset
df_1 = pd.read_csv(input_1)
df_2 = pd.read_csv(input_2)

# Filtraggio del secondo dataset in base alle condizioni richieste
df_2_filtered = df_2[(df_2["percentile_CAMS"] == 96) &
                      (df_2["percentile_AREU"] == 90) &
                      (df_2["ritardo_giorni"] == 0)]

# Unione dei dataset basata sulla corrispondenza delle date
df_merged = df_1.merge(df_2_filtered, left_on="DATA", right_on="data_AREU")

# Filtra solo le righe in cui "picchi" è True
df_filtered = df_merged[df_merged["picchi"] == True]

# Calcola la somma totale di casi_M e casi_F
totale_casi_M = df_filtered["casi_M"].sum()
totale_casi_F = df_filtered["casi_F"].sum()
totale_casi = df_filtered["casi"].sum()

# Definizione delle fasce d'età
fasce_eta = {
    "0-20": (0, 20),
    "20-30": (20, 30),
    "40-50": (40, 50),
    "50-60": (50, 60),
    "60-70": (60, 70),
    "80+": (80, float("inf")),
}

# Creazione di un dizionario per contenere i risultati
somme_fasce_eta = {}

# Calcola la somma di 'casi', 'casi_M' e 'casi_F' per ogni fascia d'età
for fascia, (min_eta, max_eta) in fasce_eta.items():
    somma_casi = df_filtered[(df_filtered["ETA"] >= min_eta) & (df_filtered["ETA"] < max_eta)]["casi"].sum()
    somma_casi_M = df_filtered[(df_filtered["ETA"] >= min_eta) & (df_filtered["ETA"] < max_eta)]["casi_M"].sum()
    somma_casi_F = df_filtered[(df_filtered["ETA"] >= min_eta) & (df_filtered["ETA"] < max_eta)]["casi_F"].sum()
    somme_fasce_eta[fascia] = [somma_casi, somma_casi_M, somma_casi_F]

# Creazione del DataFrame dei risultati
risultati_df = pd.DataFrame.from_dict(somme_fasce_eta, orient="index", columns=["Somma_Casi", "Casi_M", "Casi_F"])

# Calcola la percentuale dei casi sul totale
risultati_df["Percentuale"] = (risultati_df["Somma_Casi"] / totale_casi) * 100

# Aggiunge i totali di casi M e F
risultati_df.loc["Totale_Casi_M"] = [totale_casi_M, totale_casi_M, 0, (totale_casi_M / totale_casi) * 100]
risultati_df.loc["Totale_Casi_F"] = [totale_casi_F, 0, totale_casi_F, (totale_casi_F / totale_casi) * 100]
risultati_df.loc["Totale_Casi"] = [totale_casi, totale_casi_M, totale_casi_F, 100.0]

# Salva il dataset elaborato
risultati_df.to_csv(output_path)

# Stampa il DataFrame risultante
print(risultati_df)
