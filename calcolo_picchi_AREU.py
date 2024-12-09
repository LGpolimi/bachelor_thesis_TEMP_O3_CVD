# Importo le librerie necessarie
import pandas as pd  # Per la gestione dei dati in formato tabellare
import matplotlib.pyplot as plt  # Per la creazione dei grafici
import matplotlib.dates as mdates  # Per la personalizzazione degli assi temporali nei grafici
import os  # Per la gestione dei percorsi dei file

# Definizione dei percorsi dei file in input e output
input_dati = "/Users/lucavergani/Library/CloudStorage/OneDrive-PolitecnicodiMilano/Pycharm/dati_AREU_griglie.csv"
output_path = "/Users/lucavergani/Library/CloudStorage/OneDrive-Raccoltecondivise-PolitecnicodiMilano/Lorenzo Gianquintieri - 2425 - Analisi Epidemiologica/Picchi AREU"

# Leggo i dati dal file CSV
global_data = pd.read_csv(input_dati)

# Converto la colonna 'DATA' in formato datetime per poterla usare come variabile temporale
global_data['DATA'] = pd.to_datetime(global_data['DATA'])

# Inizializzo una lista vuota per memorizzare i dati dei giorni di picco per ogni zona
picchi_locali = []

# Chiedo all'utente di specificare il percentile che vuole analizzare
p = int(input("Inserisci il percentile (es. 90 per il 90° percentile): "))
# Nel progetto si sono studiati i percentili dal 90° al 99°, procedendo con passo 1
# Nel progetto si sono studiati i percentili dal 75° al 90°, procedendo con passo 5

# Raggruppo i dati in base a 'id_cella', ovvero per zona della griglia
for id_cella, zona_data in global_data.groupby('id_cella'):
    # Ordino i dati cronologicamente per ogni zona
    zona_data = zona_data.sort_values(by='DATA').reset_index(drop=True)

    # Calcolo il valore del percentile specificato dall'utente per una finestra mobile di 30 giorni
    zona_data['percentile_p'] = zona_data['casi'].rolling(window=30, center=True).quantile(p / 100)

    # Identifico i giorni in cui il numero di casi supera il valore del percentile calcolato
    zona_data['picco'] = zona_data['casi'] > zona_data['percentile_p']

    # Aggiungo alla lista solo i giorni in cui si è verificato un picco
    picchi_locali.append(zona_data[zona_data['picco']])

    # Creo un grafico per visualizzare, nel tempo, il numero di casi e il percentile per ogni zona
    plt.figure(figsize=(12, 6))  # Imposto la dimensione della figura

    # Traccio la serie temporale delle emergenze e del percentile
    plt.plot(zona_data['DATA'], zona_data['casi'], label=f'Segnale sanitario', linewidth=1)
    plt.plot(zona_data['DATA'], zona_data['percentile_p'], label=f'{p}° percentile', linestyle='--', color='orange')
    plt.scatter(
        zona_data['DATA'][zona_data['picco']],  # Date dei picchi
        zona_data['casi'][zona_data['picco']],  # Valori corrispondenti ai picchi
        color='red', label='Picchi', zorder=5  # Evidenzio i picchi in rosso
    )

    # Personalizzo l'asse x per mostrare le date in formato leggibile
    ax = plt.gca()  # Ottengo l'asse corrente
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Mostro anno e mese (es. "2015-01")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Etichette ogni 3 mesi
    plt.xticks(rotation=45, ha='right')  # Ruoto le etichette di 45° per maggiore leggibilità

    # Aggiungo il titolo, le etichette e la legenda al grafico
    plt.title(f'Andamento temporale dei casi per la zona {id_cella}')
    plt.xlabel('Tempo')
    plt.ylabel('Numero di emergenze')
    plt.legend()
    plt.grid()
    plt.tight_layout()  # Ottimizza lo spazio nel grafico
    plt.show()

# Unisco i dati dei picchi di tutte le zone in un unico DataFrame
picchi_locali = pd.concat(picchi_locali, ignore_index=True)

# Mostro i picchi identificati per ogni zona
for _, row in picchi_locali.iterrows():
    print(f"Zona {row['id_cella']}: Picco trovato il {row['DATA'].date()} con {row['casi']} casi")

# Salvo i dati dei picchi in un file CSV, aggiungendo il percentile nel nome del file
output_csv = os.path.join(output_path, f"Picchi_AREU({p}°percentile).csv")
picchi_locali.to_csv(output_csv, index=False)
print(f"\nFile CSV salvato con successo in: {output_csv}")

# Calcolo e stampo il numero totale di picchi trovati
num_picchi = len(picchi_locali)
print(f"\nNumero totale di picchi trovati: {num_picchi}")
