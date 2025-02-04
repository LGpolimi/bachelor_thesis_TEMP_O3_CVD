import pandas as pd

# Percorso del file di input
input_path = r"C:\Users\bruno\OneDrive\Desktop\Dati_corretti\8. Calcolo ODDS RATIO\Dati_pronti_odds\dati_ODDS.csv"

# Caricamento del file CSV
df = pd.read_csv(input_path)

# Calcolo delle somme per le diverse combinazioni
A = df[(df['picco_sanitario'] == True) & (df['picco_combinato'] == True)]['casi'].sum()
B = df[(df['picco_sanitario'] == False) & (df['picco_combinato'] == True)]['casi'].sum()
C = df[(df['picco_sanitario'] == True) & (df['picco_combinato'] == False)]['casi'].sum()
D = df[(df['picco_sanitario'] == False) & (df['picco_combinato'] == False)]['casi'].sum()

# Stampa dei risultati
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
