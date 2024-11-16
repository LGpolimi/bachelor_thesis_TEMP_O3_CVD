import os
import pandas as pd

#definisco la cartella da cui prendere i dataframe e la cartella in cui salvare il df finale
input_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\Dati grezzi\\1. AREU"
output_path = r"C:\\Users\\bruno\\OneDrive\\Desktop\\dati_elaborati\\dati_AREU_filtrati_provvisori"

#indico le colonne di interesse
columns_to_keep = [
    'SOREU', 'AAT', 'ZONA', 'COMUNE', 'PROV', 'ID_PZ', 'ID_SOCC',
    'DATA', 'ORA', 'MOTIVO', 'MOTIVO_DTL', 'GEN', 'ETA', 'ESITO_PZ',
    'LUOGO', 'LONG', 'LAT', 'DT_NUE', 'DT_118', 'INVIO_MSA1',
    'INVIO_MSA2', 'ASSISTENZA_MAX', 'CD_TRA']

#indico le parole chiave da cercare nella colonna 'MOTIVO_DTL'
keywords = ['CARDIOCIRCOLATORIA', 'RESPIRATORIA']

dataframes = []

#ciclo for per trovare i file nella cartella fornita in input
for file_name in os.listdir(input_path):
    if file_name.endswith('.tab'):
        file_path = os.path.join(input_path, file_name)

        #lettura file .tab
        df = pd.read_csv(file_path, low_memory=False, encoding='ISO-8859-1', on_bad_lines='skip', sep='\t')

        # Applica filtro sulla colonna 'MOTIVO_DTL'
        if 'MOTIVO_DTL' in df.columns:
            #rimuove spazi extra e converte in minuscolo
            df['MOTIVO_DTL'] = df['MOTIVO_DTL'].str.strip().str.lower()

            # iltra le righe che contengono le parole chiave
            df = df[df['MOTIVO_DTL'].apply(lambda x: any(keyword.lower() in str(x) for keyword in keywords))]

        #seleziona solo le colonne che ci servono
        df_filtered = df[[col for col in columns_to_keep if col in df.columns]]

        dataframes.append(df_filtered)

#unione di tutti i dataframe filtrati
if dataframes:
    final_dataframe = pd.concat(dataframes, ignore_index=True)

    #salva il dataframe finale in formato .csv nella cartella di output
    final_output_path = os.path.join(output_path, 'dati_uniti.csv')
    final_dataframe.to_csv(final_output_path, index=False)

    #visualizza informazioni sul dataframe finale
    print("Shape del dataframe unito:", final_dataframe.shape)
    print("Prime righe del dataframe unito:")
    print(final_dataframe.head())
else:
    print("Nessuna riga trovata con i criteri specificati.")
