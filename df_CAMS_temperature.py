import os
import pandas as pd

#percorso della cartella contenente i dataframe da combinare
input_folder = r"C:\Users\bruno\OneDrive\Desktop\CAMS_Temperature"

#percorso della cartella di output
output_folder = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_temperatura"
output_combined_file = os.path.join(output_folder, "combined_temperature_data.csv")
output_filtered_file = os.path.join(output_folder, "dati_CAMS_temperatura_filtrato.csv")

#elenco di tutti i file .csv nella cartella
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
if not csv_files:
    raise FileNotFoundError(f"Nessun file .csv trovato nella cartella: {input_folder}")

#creo la cartella di output se non esiste
os.makedirs(output_folder, exist_ok=True)

df_list = []

#leggo ogni file .csv e aggiungilo alla lista
for csv_file in csv_files:
    csv_file_path = os.path.join(input_folder, csv_file)
    print(f"Leggendo il file: {csv_file_path}")
    try:
        df = pd.read_csv(csv_file_path)
        df_list.append(df)
    except Exception as e:
        print(f"Errore durante la lettura del file {csv_file_path}: {e}")

#unisco tutti i DataFrame
final_df = pd.concat(df_list, ignore_index=True)

#salvo il nuovo df
final_df.to_csv(output_combined_file, index=False)
print(f"File combinato salvato con successo in: {output_combined_file}")

#filtro le colonne che mi servono
columns_to_keep = ['latitude', 'longitude', 'time', 't2m']
try:
    df_filtered = final_df[columns_to_keep]

    #salvo il file filtrato
    df_filtered.to_csv(output_filtered_file, index=False)
    print(f"File filtrato salvato con successo in: {output_filtered_file}")
except KeyError as e:
    print(f"Errore: alcune colonne specificate non esistono nel file combinato. Dettagli: {e}")
