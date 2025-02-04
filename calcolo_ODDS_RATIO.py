import pandas as pd
import os

# Percorso della cartella che contiene i file CSV
folder_path = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\8. Calcolo ODDS RATIO\Dati_pronti_odds"

# Ciclo su ogni numero da 0 a 4 per caricare i file corrispondenti
for numero in range(5):
    # Costruzione del nome del file
    file_name = f"dati_ODDS_delay_{numero}.csv"
    input_path = os.path.join(folder_path, file_name)

    # Verifica che il file esista
    if os.path.exists(input_path):
        # Caricamento del file CSV
        df = pd.read_csv(input_path)

        # Calcolo delle somme per le diverse combinazioni
        A = df[(df['picco_sanitario'] == True) & (df['picco_combinato'] == True)]['casi'].sum()
        B = df[(df['picco_sanitario'] == False) & (df['picco_combinato'] == True)]['casi'].sum()
        C = df[(df['picco_sanitario'] == True) & (df['picco_combinato'] == False)]['casi'].sum()
        D = df[(df['picco_sanitario'] == False) & (df['picco_combinato'] == False)]['casi'].sum()

        # Stampa dei risultati per ogni file
        print(f"\nFile: {file_name}")
        print(f"A = {A}")
        print(f"B = {B}")
        print(f"C = {C}")
        print(f"D = {D}")

        # Calcolo e stampa del rapporto A*D / B*C
        if B * C == 0:
            print("Odds Ratio = ∞")
        else:
            odds_ratio = (A * D) / (B * C)
            print(f"Odds Ratio = {odds_ratio}")
    else:
        print(f"Il file {file_name} non esiste nella cartella.")

