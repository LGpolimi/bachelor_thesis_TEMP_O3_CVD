import pandas as pd
import glob
import os

# Definisco la cartella dove si trovano i file AREU
percorso = r"C:\Users\bruno\OneDrive\Desktop\Dati grezzi\1. AREU"

# Indico dove salvare i dati filtrati
output_df = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_AREU_filtrati"

# Assicuro che la cartella di output esista
os.makedirs(output_df, exist_ok=True)

# Ciclo per pulire e filtrare i file AREU dal 2015 al 2023
for anno in range(2015, 2023 + 1):
    pattern = os.path.join(percorso, f"EVT_MISS_PZ_{anno}*.tab")
    files = glob.glob(pattern)

    # Controllo se ci sono file corrispondenti all'anno specifico
    print(f"Elaboro i file per l'anno {anno}: {files}")
    if not files:
        print(f"Nessun file trovato per l'anno {anno}")

    for file in files:
        try:
            # Carico il file
            df = pd.read_csv(file, low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep='\t')

            # Rimuovo le righe con valori mancanti e resetto l'indice
            df.dropna(inplace=True)
            df.reset_index(drop=True, inplace=True)

            # Seleziono le colonne necessarie
            colonne_richieste = ['COMUNE', 'PROV', 'ID_PZ', 'ID_SOCC', 'DATA', 'ORA',
                                 'MOTIVO', 'MOTIVO_DTL', 'GEN', 'ETA', 'ESITO_PZ',
                                 'LUOGO', 'LONG', 'LAT', 'DT_NUE',
                                 'INVIO_MSA1', 'INVIO_MSA2', 'ASSISTENZA_MAX', 'CD_TRA']

            # Verifico che le colonne richieste esistano nel DataFrame
            colonne_mancanti = [col for col in colonne_richieste if col not in df.columns]
            if colonne_mancanti:
                print(f"Colonne mancanti nel file {file}: {colonne_mancanti}")
                continue

            # Seleziono solo le colonne richieste
            df_filtrato1 = df[colonne_richieste]

            # Filtro le righe dove 'MOTIVO_DTL' è 'CARDIOCIRCOLATORIA'
            df_filtrato2 = df_filtrato1[df_filtrato1['MOTIVO_DTL'].isin(['CARDIOCIRCOLATORIA', 'RESPIRATORIA'])]
            df_filtrato2.reset_index(drop=True, inplace=True)

            # Salvo il DataFrame filtrato in un nuovo file CSV
            nome_file = os.path.basename(file)  # Recupera il nome del file originale
            df_filtrato2.to_csv(os.path.join(output_df, nome_file), index=False, sep='\t')

        except Exception as e:
            print(f"Errore nell'elaborazione del file {file}: {e}")
