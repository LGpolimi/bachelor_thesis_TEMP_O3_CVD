'''
codice per il calcolo degli odd ratio e degli intervalli di confidenza al 95%
'''

import pandas as pd
import os
import numpy as np

# Percorso del file specifico da analizzare
input_path = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\8. Calcolo ODDS RATIO\Dati_pronti_odds\dati_ODDS.csv"

# Verifica che il file esista
if os.path.exists(input_path):
    # Caricamento del file CSV
    df = pd.read_csv(input_path)

    # Calcolo delle somme per le diverse combinazioni
    A = df[(df['picco_sanitario'] == True) & (df['picco_CAMS'] == True)]['casi'].sum()
    B = df[(df['picco_sanitario'] == False) & (df['picco_CAMS'] == True)]['casi'].sum()
    C = df[(df['picco_sanitario'] == True) & (df['picco_CAMS'] == False)]['casi'].sum()
    D = df[(df['picco_sanitario'] == False) & (df['picco_CAMS'] == False)]['casi'].sum()

    # Stampa dei risultati
    print(f"\nFile: {input_path}")
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"C = {C}")
    print(f"D = {D}")

    # Calcolo e stampa del rapporto A*D / B*C
    if B * C == 0:
        print("Odds Ratio = ∞")
        print("Intervallo di confidenza non calcolabile")
    else:
        odds_ratio = (A * D) / (B * C)
        log_or = np.log(odds_ratio)  # Logaritmo naturale dell'OR

        # Calcolo dell'errore standard (SE)
        se_log_or = np.sqrt((1/A) + (1/B) + (1/C) + (1/D))

        # Limiti di confidenza
        z_value = 1.96  # Per un intervallo di confidenza del 95%
        lower_log = log_or - z_value * se_log_or
        upper_log = log_or + z_value * se_log_or

        # Conversione dall'unità logaritmica
        lower_ci = np.exp(lower_log)
        upper_ci = np.exp(upper_log)

        print(f"Odds Ratio = {odds_ratio}")
        print(f"Intervallo di confidenza al 95%: ({lower_ci}, {upper_ci})")
else:
    print(f"Il file {input_path} non esiste.")