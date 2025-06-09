# Progetto Universitario Graboid-RFC

**Graboid-RFC** è un progetto orientato allo sviluppo di un sistema per l'indicizzazione e la ricerca efficace di **documenti RFC** (Request for Comments); documenti tecnici di fondamentale importanza nel campo delle telecomunicazioni e dell'informatica.

L'obiettivo principale è sviluppare e **confrontare le prestazioni** di tre diversi motori di ricerca, basati sui seguenti sistemi: **PostgreSQL**, **PyLucene**, **Whoosh**; applicati alla collezione di documenti RFC.

La documentazione e le slide del progetto si trovano nella cartella: `./gestione-info/workspace/docs/`.

<!--
### Struttura del Progetto 

Lo schema seguente mostra l'organizzazione generale di file e cartelle nella gerarchia del progetto, evidenziando le componenti che potrebbero interessarle maggiormente.

```bash
gestione-info/
│
├─── graboidrfc/
│    │
│    ├─── core/
│    │    │
│    │    ├─── modules/
│    │    │    │
│    │    │    └─── engines/    # Tre sistemi, il parser, calcolo del benchmark
│    │    │    
│    │    ├─── data/            # Dataset, indici invertiti e benchmark
│    │    └─── config/          # I File di configurazione dell'applicazione
│    │
│    └─── main.py
│
├─── workspace/
│    │
│    └─── docs/                 # Documentazione e Presentazione del progetto
│
├─── scripts/                   # Scripts di installazione delle dipendenze
└─── setup.py
```
-->

<!-- https://symbl.cc/en/unicode/blocks/box-drawing/ -->

# Setup (Febbraio 2025)

### Premesse

1. Il processo di installazione del pacchetto e delle relative dipendenze è stato adattato e testato su sistemi:

    - **Ubuntu**
    - **Debian**
    - **Ubuntu su WSL2 (Windows 11)**

    Sconsigliamo l'utilizzo su altri sistemi operativi, perchè non sono stati testati. Nel caso in cui non si disponga di una macchina con quei sistemi operativi, si consiglia l'uso di un **hypervisor**.

2. Durante l'installazione delle dipendenze, potrebbe essere necessario eseguire occasionalmente degli script situati nella directory  `./gestione-info/scripts/`.

### Dipendenze

Per la corretta installazione e il funzionamento del pacchetto, è necessario installare le seguenti dipendenze nel caso non fossero già soddisfatte:

<!--- **[Docker](#docker)** $\rightarrow$ Per la gestione del container (PostgreSQL).
    - **qemu, libvirt, ovmf, etc.** $\rightarrow$ Necessari per abilitare la virtualizzazione. -->

1. **[PostgreSQL](#installazione-postgresql-e-setup-del-database)** $\rightarrow$ Uno dei tre sistemi che utilizziamo per effettuare Full-Text Search.
    - Creazione e setup del database e attribuzione permessi all'utente.

2. **[Anaconda](#installazione-anaconda)** $\rightarrow$ Per la gestione dell'ambiente Python.
    - **python** $\rightarrow$ ($\geq$ **3.10**, consigliata: **3.12.7**) Per eseguire il nostro pacchetto.
    - **pip** $\rightarrow$ Per l'installazione dei pacchetti Python.

3. **[PyLucene](#installazione-pylucene)** $\rightarrow$ ($\geq$ **9.4.1**) Uno dei tre sistemi che utilizziamo per effettuare Full-Text Search.
    - **Java 17 (JDK)** $\rightarrow$ Necessario per l'uso di PyLucene.
    - **JCC** $\rightarrow$ Necessario per l'uso di PyLucene.
    - **Make** $\rightarrow$ Necessario per l'installazione di PyLucene.
    - **Ant** $\rightarrow$ Necessario per l'installazione di PyLucene.

Soddisfatte tutte le dipendenze sarà possibile [installare il nostro pacchetto](#installazione-pacchetto), seguendo la procedura.

---

### Installazione PostgreSQL e Setup del Database

L'obiettivo di questa fase è assicurarsi che il servizio PostgreSQL sia attivo sul sistema e creare il database e l'utente necessari per il pacchetto.

- **Installazione e attivazione del servizio PostgreSQL**

    Aggiorna i pacchetti e installa PostgresSQL insieme ai pacchetti aggiuntivi:

    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```

    Assicurati che il servizio PostgreSQL sia avviato e configurato per partire automaticamente al riavvio del sistema:

    ```bash
    sudo systemctl start postgresql.service  # avvia il servizio
    sudo systemctl status postgresql.service # controlla che il servizio sia attivo
    sudo systemctl enable postgresql.service # abilita il servizio ad ogni riavvio
    ```
    
    Imposta una password per l'utente `postgres` eseguendo il seguente comando:

    ```bash
    sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
    ```

    > **Nota** La password predefinita per l'utente predefinito `postgres` è "postgres". Potrebbe essere richiesta nelle fasi successive.

- **Creazione del database e dell'utente**

    Lo script `setup_postgres.sh` automatizza la creazione del database e dell'utente che il nostro pacchetto utilizza, e garantisce che l'utente abbia i permessi necessari.

    ```bash
    chmod +x setup_postgres.sh
    ./setup_postgres.sh
    ```

- **Specificare la porta del servizio PostgreSQL**

    Se il servizio PostgreSQL non sta usando la porta predefinita `5432`, dovrai aggiornare il file di configurazione del progetto prima della sua installazione.

    **Modifica della porta:**

    - [Clona](#installazione-pacchetto) il nostro repository, ma non installarlo.
    - Apri il file `./gestione-info/graboidrfc/core/config/postgres.json`.
    - Modifica il campo `PORT_NUMBER` con il numero di porta corretto a cui PostgreSQL è in ascolto.

---

### Installazione Anaconda 

L'obiettivo di questa fase è creare un ambiente virtuale isolato in cui poter installare PyLucene. L'installazione di PyLucene è complessa e l'unico metodo che abbiamo trovato è eseguire l'installazione all'interno di un ambiente virtuale gestito da **Anaconda**. 

- **Scaricare e installare Anaconda**

    Prima di iniziare, assicurarsi che **curl** sia installato:

    ```bash
    sudo apt update && sudo apt install curl -y
    ```

    Scaricare l'installer ufficiale di **Anaconda** per Linux:

    ```bash
    curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
    ```

    Eseguire lo script di installazione:

    ```bash
    bash Anaconda3-2024.02-1-Linux-x86_64.sh
    ```

    Durante l'installazione:

    - **Premere** `ENTER` per continuare.
    - **Accettare la licenza** digitando `yes`.
    - **Confermare il percorso di installazione** (premere `ENTER` per il percorso predefinito).
    - **Quando viene chiesto di inizializzare Anaconda**, digitare `yes`.

- **Abilitare Anaconda nella sessione**

    Dopo l'installazione, attivare Anaconda ed eseguire l'inizializzazione:

    ```bash
    source $HOME/anaconda3/bin/activate
    conda init
    source $HOME/.bashrc
    ```

- **Creare l'ambiente dedicato a PyLucene**

    Creare un nuovo ambiente virtuale chiamato `lucene` con Python:

    ```bash
    conda create -n lucene python=3.12.7
    ```

    Attivare l'ambiente:
 
    ```bash
    conda activate lucene
    ```

    > **Nota** Ogni volta che apri una nuova sessione della shell, dovrai riattivare l'ambiente eseguendo nuovamente questo comando.

---

### Installazione PyLucene

Eseguire i seguenti passaggi all'interno dell'**ambiente Anaconda dedicato** creato al punto precedente, per garantire che tutte le dipendenze siano correttamente gestite.

- **Installazione dei pacchetti necessari alla build**

    Per buildare PyLucene, è necessario installare alcuni pacchetti:

    ```bash
    sudo apt update
    sudo apt install openjdk-17-jdk python3 python3-pip python3-setuptools ant gcc g++ make
    ```

- **Build e Installazione di PyLucene**

    Lo script `setup_pylucene.sh` automatizza il processo di **installazione di PyLucene**:

    ```bash
    chmod +x setup_pylucene.sh
    ./setup_pylucene.sh
    ```

- **Rendere Permanenti le Variabili d'Ambiente**

    Una volta completata l'installazione, è necessario **rendere permanenti le variabili d'ambiente** aggiungendole al file `.bashrc`. Lo script `setup_variables` automatizza questo processo:

    ```bash
    chmod +x setup_variables.sh
    ./setup_variables.sh
    ```

    Dopo aver eseguito lo script, è necessario riavviare il terminale oppure rieseguire il file per aggiornare l'ambiente della sessione corrente con le nuove variabili:

    ```bash
    source $HOME/.bashrc
    ```

    Tuttavia, questo può riportarti all'ambiente di default di Anaconda (`base`). Per lavorare con PyLucene, è necessario riattivare l'ambiente corretto:

    ```bash
    conda activate lucene
    ```

- **Verifica dell'Installazione**

    Per verificare che l'installazione di PyLucene sia stata completata correttamente, esegui il seguente comando. Se non ci sono errori, l'installazione è stata completata con successo.

    ```bash
    python -c "import lucene; lucene.initVM()"
    ```

---

### Installazione Pacchetto

Una volta soddisfatte le dipendenze, sarà possibile procedere con l'installazione del pacchetto utilizzando `pip`. Si consiglia di eseguire l'installazione all'interno di un **ambiente virtuale** Python gestito tramite Anaconda, lo stesso ambiente in cui è installato PyLucene.

- **Clonare il repository GitHub**
    
    ```bash
    git clone https://github.com/Tremors3/gestione-info.git
    ```

- **Navigare nella cartella del progetto e installare il pacchetto**

    ```bash
    cd gestione-info
    pip install .
    ```

- **Inizializzare l'applicazione con il seguente comando**

    ```bash
    graboidrfc --init
    ```

    L'inizializzazione effettua le seguenti seguenti operazioni:

    - Scarica e prepara il dataset
    - Inizializza e popola il database
    - Crea gli indici per i tre motori di ricerca

    In caso di errori durante l'esecuzione del comando:

    > **Nota** Se si verifica un errore durante una delle fasi precedenti, è possibile rieseguire solo quella specifica fase senza ripetere le precedenti, risparmiando tempo. Per maggiori dettagli, consultare la sezione [Debugging Installazione](#debug-installazione-pacchetto).

### Debug Installazione Pacchetto

- Se si verifica un errore durante il download del dataset, e si intende riprovare, eseguire il comando:

    ```
    graboidrfc --init
    ```

- Se l'errore riguarda il collegamento al database, il popolamento dei dati o la creazione degli indici, è possibile ripetere la fase corrispondente senza dover scaricare nuovamente il dataset già acquisito:

    ```
    graboidrfc --indexes
    ```

    In generale, per problemi di indicizzazione, si **sconsiglia** di eseguire nuovamente l'inizializzazione completa con `--init` poiché comporta il download del dataset già acquisito.

### Avvio dell'Applicazione

- Per avviare l'applicazione, eseguire il comando:

    ```bash
    graboidrfc --start
    ```

    Il comando avvia un servizio web locale all'indirizzo `127.0.0.1:5000`, attraverso il quale è possibile interagire con i tre motori di ricerca.

### Costruzione dei Grafici

- Per generare i grafici, eseguire il comando:

    ```
    graboidrfc --graphs
    ```

    Al termine dell'operazione, che potrebbe richiedere alcuni secondi, verrà visualizzato il percorso in cui i grafici sono stati salvati.

### Elenco argomenti dell'applicazione

<table style="width:100%; table-layout: fixed;">
    <tr>
        <td style="width:1%">Mostra tutte le opzioni</td>
        <td style="width:1%"><code>graboidrfc -h, --help</code></td>
    </tr>
    <tr>
        <td style="width:1%">Inizializza l'applicazione</td>
        <td style="width:1%"><code>graboidrfc -i, --init</code></td>
    </tr>
    <tr>
        <td style="width:1%">Debug: Esecuzione del parser</td>
        <td style="width:1%"><code>graboidrfc -p, --parser</code></td>
    </tr>
    <tr>
        <td style="width:1%">Debug: Costruzione degli indici</td>
        <td style="width:1%"><code>graboidrfc -x, --indexes</code></td>
    </tr>
    <tr>
        <td style="width:1%">Avvia l'applicazione</td>
        <td style="width:1%"><code>graboidrfc -s, --start</code></td>
    </tr>
    <tr>
        <td style="width:1%">Costruzione dei grafici</td>
        <td style="width:1%"><code>graboidrfc -g, --graphs</code></td>
    </tr>
</table> 

Nel caso si voglia visualizzare l'intera lista di argomenti utilizzare l'opzione `-h` o `--help`.

## Collaboratori

<h4 align="left">
    <ul>
        <li>Matteo Menozzi <a href="https://github.com/Tremors3" style="vertical-align: middle;"><img src="https://badgen.net/badge/github/Tremors3/?icon=github"></a></li>
        <li>Enrico Turci Sologni <a href="https://github.com/HerryTS" style="vertical-align: middle;"><img src="https://badgen.net/badge/github/HerryTS/?icon=github"></a></li>
        <li>Gabriele Turci <a href="https://github.com/Gabeee88" style="vertical-align: middle;"><img src="https://badgen.net/badge/github/Gabeee88/?icon=github"></a></li>
    </ul>
</h4>
