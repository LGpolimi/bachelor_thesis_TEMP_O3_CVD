'''
diverse operazioni:
- pre elaborazione colonna time (se serve)
- unione dei dati CAMS ozono e temperatura
    sulla stessa riga ho le informazioni su data, id_cella, temperatura, ozono
- eseguo operazione di eliminazione/attenuazione degli outliers
- effettuo operazione di normalizzazione e somma dei dati
- aggiungo una colonna con il dato normalizzato per ogni cella e per ogni data
- valuto i grafici
'''

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

#percorsi dei file di input/output
input_ozono = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_griglie\dati_ozono_griglie.csv"
input_temperature = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_griglie\dati_temperatura_griglie.csv"
output_path = r"C:\Users\bruno\OneDrive\Desktop\dati_elaborati\dati_CAMS_uniti_normalizzati"

#funzione per pre-elaborazione della colonna 'time'
'''anche se i dati erano già stati salvati in formato datetime questi venivano gestiti scorrettamente dal codice
    - venivano letti in formato errato '1970-01-01 00:00:00.020150101' 
    - estraggo solo gli ultimi 8 caratteri
    - li converto successivamente in formato datetime
'''

def preprocess_time_column(df, time_column='time'):
    #estrazione degli ultimi 8 caratteri per ottenere la data in formato 'yyyyMMdd'
    df[time_column] = df[time_column].astype(str).str[-8:]

    #converto dei dati estratti in formato datetime
    try:
        df[time_column] = pd.to_datetime(df[time_column], format='%Y%m%d', errors='coerce')
    except Exception as e:
        print(f"Errore nella conversione della colonna {time_column}: {e}")
        return df

    #identifico valori non validi
    invalid_dates = df[df[time_column].isna()]
    if not invalid_dates.empty:
        print(f"Date non valide trovate: {len(invalid_dates)}")
        print(invalid_dates.head())

    #rimuovo le date non valide
    df = df.dropna(subset=[time_column])
    print(f"Time column preprocessed. Head of dataframe:\n{df.head()}")
    return df

#leggo i dati
ozono_data = pd.read_csv(input_ozono)
temperature_data = pd.read_csv(input_temperature)

#pre-elaborazione della colonna 'time'
ozono_data = preprocess_time_column(ozono_data, time_column='time')
temperature_data = preprocess_time_column(temperature_data, time_column='time')

#rinomino la colonna 'mean_value' per distinguere i dataset dopo l'unione
ozono_data = ozono_data.rename(columns={'mean_value': 'ozono'})
temperature_data = temperature_data.rename(columns={'mean_value': 'temperatura'})

#unione dei dati su 'time' e 'LMB3A_IDcu'
merged_data = pd.merge(
    ozono_data[['LMB3A_IDcu', 'time', 'ozono', 'latitude', 'longitude']],
    temperature_data[['LMB3A_IDcu', 'time', 'temperatura']],
    on=['LMB3A_IDcu', 'time'],
    how='inner'
)

#gestione degli outliers
def remove_outliers(df, columns):
    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    print(f"Outliers removed for columns {columns}.")
    return df

merged_data = remove_outliers(merged_data, ['ozono', 'temperatura'])

#normalizzazione dei dati
scaler = MinMaxScaler()
merged_data[['ozono_normalized', 'temperatura_normalized']] = scaler.fit_transform(merged_data[['ozono', 'temperatura']])

#aggiunta di colonna normalizzata e calcolo della somma
merged_data['sum_normalized'] = merged_data['ozono_normalized'] + merged_data['temperatura_normalized']

# Esportazione dei dati
os.makedirs(output_path, exist_ok=True)
output_file = os.path.join(output_path, 'dati_uniti_normalizzati.csv')
merged_data.to_csv(output_file, index=False)

print(f"File esportato con successo in: {output_file}")

#funzione per la creazione e il salvataggio dei grafici di prova
def save_plot(df, x_col, y_col, title, output_folder, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], label=y_col, color='blue')
    plt.xlabel(x_col)
    plt.ylabel('Values')
    plt.title(title)
    plt.legend()
    plt.grid()
    output_file = os.path.join(output_folder, filename)
    plt.savefig(output_file)
    print(f"Grafico salvato in: {output_file}")
    plt.close()

#salvo i grafici separati per ozono e temperatura
save_plot(merged_data, 'time', 'ozono_normalized', 'Normalized Ozone Over Time', output_path, 'ozono_normalized_plot.png')
save_plot(merged_data, 'time', 'temperatura_normalized', 'Normalized Temperature Over Time', output_path, 'temperatura_normalized_plot.png')
