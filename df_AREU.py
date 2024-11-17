import os
import pandas as pd

# "mappa" dei mesi abbreviati al loro valore numerico
mesi_map = {
    'GEN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAG': '05', 'GIU': '06',
    'LUG': '07', 'AGO': '08', 'SET': '09', 'OTT': '10', 'NOV': '11', 'DIC': '12',
    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
    'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
}

# Definisco la cartella da cui prendere i dataframe e la cartella in cui salvare il df finale
input_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\Dati grezzi\\1. AREU"
output_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_elaborati\\dati_AREU_filtrati_provvisori"

# Indico le colonne di interesse
columns_to_keep = [
    'SOREU', 'AAT', 'ZONA', 'COMUNE', 'PROV', 'ID_PZ', 'ID_SOCC',
    'DATA', 'ORA', 'MOTIVO', 'MOTIVO_DTL', 'GEN', 'ETA', 'ESITO_PZ',
    'LUOGO', 'LONG', 'LAT', 'DT_NUE', 'DT_118', 'INVIO_MSA1',
    'INVIO_MSA2', 'ASSISTENZA_MAX', 'CD_TRA']

# Indico le parole chiave da cercare nella colonna 'MOTIVO_DTL'
keywords = ['CARDIOCIRCOLATORIA', 'RESPIRATORIA']

dataframes = []

# Ciclo for per trovare i file nella cartella fornita in input
for file_name in os.listdir(input_path):
    if file_name.endswith('.tab'):
        file_path = os.path.join(input_path, file_name)

        df = pd.read_csv(file_path, low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep='\t')

        # Applico filtro sulla colonna 'MOTIVO_DTL'
        if 'MOTIVO_DTL' in df.columns:
            # Rimuove spazi extra e converte in minuscolo
            df['MOTIVO_DTL'] = df['MOTIVO_DTL'].str.strip().str.lower()

            # Filtro le righe che contengono le parole chiave
            df = df[df['MOTIVO_DTL'].apply(lambda x: any(keyword.lower() in str(x) for keyword in keywords))]

        # Seleziona solo le colonne che ci servono
        df_filtered = df[[col for col in columns_to_keep if col in df.columns]]

        # Aggiungo il dataframe filtrato alla lista
        dataframes.append(df_filtered)

# Unisco tutti i dataframe filtrati
if dataframes:
    final_dataframe = pd.concat(dataframes, ignore_index=True)

    if 'DATA' in final_dataframe.columns:
        # Isolo solo la parte della data prima dei due punti
        final_dataframe['DATA'] = final_dataframe['DATA'].str.split(':').str[0]

        # Sostituisco i mesi abbreviati con il formato numerico
        for mese, numero in mesi_map.items():
            final_dataframe['DATA'] = final_dataframe['DATA'].str.replace(mese, numero, regex=True)

        # Converto la colonna DATA in formato datetime
        final_dataframe['DATA'] = pd.to_datetime(
            final_dataframe['DATA'],
            format='%d%m%Y',
            errors='coerce'  # Ignora valori non validi e li imposta come NaT
        )

    # Elimina righe duplicate per lo stesso paziente nello stesso giorno
    if 'ID_PZ' in final_dataframe.columns and 'DATA' in final_dataframe.columns:
        final_dataframe = final_dataframe.drop_duplicates(subset=['ID_PZ', 'DATA'])

    #Riempie i valori mancanti nella colonna 'ETA' con la media delle età
    if 'ETA' in final_dataframe.columns:
        # Converte la colonna ETA in numerico per calcolare la media
        final_dataframe['ETA'] = pd.to_numeric(final_dataframe['ETA'], errors='coerce')
        media_eta = final_dataframe['ETA'].mean(skipna=True)
        final_dataframe['ETA'] = final_dataframe['ETA'].fillna(media_eta)
        print(media_eta)

    #Salvo il dataframe finale in formato .csv nella cartella di output
    final_output_path = os.path.join(output_path, 'dati_uniti.csv')
    final_dataframe.to_csv(final_output_path, index=False)

    #Visualizzo alcune informazioni sul dataframe finale
    print("Shape del dataframe unito:", final_dataframe.shape)
    print("Prime righe del dataframe unito:")
    print(final_dataframe[['DATA']].head())
else:
    print("Nessuna riga trovata con i criteri specificati.")