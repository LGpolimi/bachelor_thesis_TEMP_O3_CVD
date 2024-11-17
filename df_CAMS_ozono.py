import os
import xarray as xr
import pandas as pd

#percorsi delle cartelle di input e output
input_folder = r"C:\Users\bruno\OneDrive\Desktop\Dati grezzi\2. CAMS_O3"
output_folder = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_ozono2"

dataframes = []

#ciclo for per trovare i file nella cartella input
for file in os.listdir(input_folder):
    if file.endswith('.nc'):
        file_path = os.path.join(input_folder, file)

        try:
            ds = xr.open_dataset(file_path)
            df = ds.to_dataframe().reset_index()

            #controllo che ci siano le colonne necessarie
            if 'lat' in df.columns and 'lon' in df.columns and 'time' in df.columns:
                #salvo le date in formato 'datetime'
                df['time'] = pd.to_datetime(df['time'])

                df_sorted = df.sort_values(by=['lat', 'lon', 'time'])

                df_filtered = df_sorted.groupby(['lat', 'lon']).first().reset_index()

                #salvataggio del singolo DataFrame filtrato in un file CSV
                csv_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_filtered.csv")
                df_filtered.to_csv(csv_file_path, index=False)

                #aggiungo il dataFrame filtrato alla lista
                dataframes.append(df_filtered)
            else:
                print(f"Il file {file} non contiene le colonne richieste ('lat', 'lon', 'time').")
        except Exception as e:
            print(f"Errore durante l'elaborazione del file {file}: {e}")

#unisco tutti i dataFrame filtrati in un unico DataFrame
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)

    #rinomino le colonne 'lat' e 'lon' in 'latitude' e 'longitude'
    combined_df.rename(columns={'lat': 'latitude', 'lon': 'longitude'}, inplace=True)

    #salvo il dataFrame in un file CSV
    combined_csv_path = os.path.join(output_folder, "dati_CAMS_ozono.csv")
    combined_df.to_csv(combined_csv_path, index=False)

    print(f"Elaborazione completata. File combinato salvato in: {combined_csv_path}")
else:
    print("Non ci sono dati validi da combinare.")