# Progetto Universitario Graboid-RFC

**Graboid-RFC** è un progetto orientato allo sviluppo di un sistema per l'indicizzazione e la ricerca efficace di **documenti RFC** (Request for Comments); documenti tecnici di fondamentale importanza nel campo delle telecomunicazioni e dell'informatica.

L'obiettivo principale è sviluppare e **confrontare le prestazioni** di tre diversi motori di ricerca (PostgreSQL, PyLucene, Whoosh) applicati al alla collezione di document RFC.

<!--
### Tecnologie Utilizzate

Le principali tecnologie utilizzate nello sviluppo del progetto sono:

- **PostgreSQL** $\rightarrow$ Database relazionale con supporto per full-text search.

- **PyLucene** $\rightarrow$ Implementazione Python di Apache Lucene, motore di ricerca ad alte prestazioni.

- **Whoosh** $\rightarrow$ Libreria Python per la gestione di motori di ricerca testuali.
 
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
└─── setup.py
```
-->

<!-- https://symbl.cc/en/unicode/blocks/box-drawing/ -->

<br />

## Setup

### 👉 Premessa

Il processo di installazione del pacchetto e delle relative dipendenze è stato **adattato e testato su sistemi Ubuntu, Debian e Ubuntu su WSL2 (Windows 11)**.

Sconsigliamo l'utilizzo su altri sistemi operativi, poiché non sono stati testati. Nel caso in cui non si disponga di una macchina con quei sistemi operativi, si consiglia l'uso di un **hypervisor**.

<br />

### 👉 Dipendenze 

Per la corretta installazione e il funzionamento del pacchetto, è necessario installare le seguenti dipendenze nel caso non fossero già soddisfatte:


<!--- **[🔧 Docker](#docker)** $\rightarrow$ Per la gestione del container (PostgreSQL).
    - **qemu, libvirt, ovmf, etc.** $\rightarrow$ Necessari per abilitare la virtualizzazione. -->

1. **[🔧 PostgreSQL](#-installazione-postgresql-e-setup-del-database)** $\rightarrow$ Uno dei tre sistemi che utilizziamo per effettuare Full-Text Search.
    - Creazione di database ed utente e selezione della porta.

2. **[🔧 Anaconda](#-installazione-anaconda)** $\rightarrow$ Per la gestione dell'ambiente Python.
    - **python** $\rightarrow$ ($\geq$ **3.10**, consigliata: **3.12.7**) Fondamentale per eseguire il nostro pacchetto.
    - **pip** $\rightarrow$ Per l'installazione dei pacchetti Python.

3. **[🔧 PyLucene](#-installazione-pylucene)** $\rightarrow$ ($\geq$ **9.4.1**) Uno dei tre sistemi che utilizziamo per effettuare Full-Text Search.
    - **Java 17 (JDK)** $\rightarrow$ Necessario per l'uso di PyLucene.
    - **JCC** $\rightarrow$ Necessario per l'uso di PyLucene.
    - **Make** $\rightarrow$ Necessario per l'installazione di PyLucene.
    - **Ant** $\rightarrow$ Necessario per l'installazione di PyLucene.

4. **🔧 git** $\rightarrow$ Per clonare il repository.

Soddisfatte tutte le dipendenze sarà possibile [installare il nostro pacchetto](#-installazione-pacchetto), seguendo la procedura.

<br />

### 👉 Installazione Pacchetto

Per installare il pacchetto, utilizzeremo `pip`. È consigliabile eseguire l'installazione all'interno di un ambiente virtuale Python, gestito ad esempio tramite **Anaconda** (lo stesso ambiente in cui è installato PyLucene).

- **📌 Clonare il repository GitHub**
    
    ```bash
    git clone https://github.com/Tremors3/gestione-info.git
    ```

- **📌 Navigare nella cartella del progetto e installare il pacchetto**

    ```bash
    cd gestione-info
    pip install .
    ```

- **📌 Inizializzare l'applicazione con il seguente comando**

    ```bash
    graboidrfc --init
    ```

    L'inizializzazione effettua le seguenti seguenti operazioni:

    - Scarica e prepara il dataset
    - Crea il container Docker per PostgreSQL
    - Crea e popola il database
    - Crea gli indici per i tre motori di ricerca

- **📌 Avvio dell'Applicazione**

    Per avviare l'applicazione, eseguire il comando:

    ```bash
    graboidrfc --start
    ```

    Il comando avvia un servizio web locale all'indirizzo `127.0.0.1:5000`, attraverso il quale è possibile interagire con i tre motori di ricerca.

<br />

### 👉 Installazione PostgreSQL e Setup del Database

- **📌 Installazione e attivazione del servizio PostgreSQL**

    Procedi con l'installazione di PostgreSQL:

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
    
    Imposta una password per l'utente postgres eseguendo il seguente comando:

    ```bash
    sudo -u postgres psql
    ```

    Una volta dentro la console di PostgreSQL, imposta la password con il comando:

    ```sql
    ALTER USER postgres WITH PASSWORD 'postgres';
    ```

    **Nota**: La password predefinita per l'utente predefinito `postgres` è `postgres`. Sarà richiesta nelle fasi successive.

- **📌 Creazione del database e dell'utente**

    Il seguente script automatizza la creazione del database e dell'utente che il nostro pacchetto utilizza, e garantisce che l'utente abbia i permessi necessari.

    ```bash
    #!/bin/bash
    set -e

    DB_NAME="graboid_rfc"
    DB_USER="graboid"
    DB_PASS="graboid"

    # Verifica se PostgreSQL è in esecuzione
    if ! systemctl is-active --quiet postgresql; then
        echo "Avvia PostgreSQL prima di eseguire lo script."
        exit 1
    fi

    # Funzione per verificare se il database esiste
    check_db_exists() {
        sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$1'" | grep -q 1
    }

    # Funzione per verificare se l'utente esiste
    check_user_exists() {
        sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$1'" | grep -q 1
    }

    # Crea il database se non esiste
    if ! check_db_exists $DB_NAME; then
        echo "Creazione del database '$DB_NAME'..."
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    fi

    # Crea l'utente se non esiste
    if ! check_user_exists $DB_USER; then
        echo "Creazione dell'utente '$DB_USER'..."
        sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
        sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    fi

    echo "L'utente '$DB_USER' ha i permessi sul database '$DB_NAME'."
    ```

- **📌 Specificare la porta del servizio PostgreSQL**

    Se il servizio PostgreSQL non sta usando la porta predefinita `5432`, dovrai aggiornare il file di configurazione del progetto.

    **Modifica della porta:**

    1. [Clona](#👉-installazione-pacchetto) il nostro repository, ma non installarlo.
    2. Apri il file `./gestione-info/graboidrfc/core/config/postgres.json`.
    3. Modifica il campo `PORT_NUMBER` con il numero di porta corretto a cui PostgreSQL è in ascolto.

<br />

### 👉 Installazione Anaconda 

- **📌 Scaricare e installare Anaconda**

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

    1. **Premere** `ENTER` per continuare.
    2. **Accettare la licenza** digitando `yes`.
    3. **Confermare il percorso di installazione** (premere `ENTER` per il percorso predefinito).
    4. **Quando viene chiesto di inizializzare Anaconda**, digitare `yes`.

- **📌 Abilitare Anaconda nella sessione**

    Dopo l'installazione, attivare Anaconda ed eseguire l'inizializzazione:

    ```bash
    source ~/.bashrc
    conda init
    ```

- **📌 Creare l'ambiente dedicato a PyLucene**

    Creare un nuovo ambiente virtuale chiamato `lucene` con Python:

    ```bash
    conda create -n lucene python=3.12.7
    ```

    Attivare l'ambiente:

    ```bash
    conda activate lucene
    ```

    Ogni volta che apri una nuova sessione della shell, dovrai riattivare l'ambiente eseguendo nuovamente questo comando.

<br />

### 👉 Installazione PyLucene

Si consiglia di eseguire i seguenti passaggi all'interno di un **ambiente Anaconda dedicato**, per garantire che tutte le dipendenze siano correttamente gestite.

- **📌 Installazione dei pacchetti necessari alla build**

    Per costruire PyLucene, è necessario installare alcuni pacchetti:

    ```bash
    sudo apt update
    sudo apt install openjdk-17-jdk python3 python3-pip python3-setuptools ant gcc make
    ```

- **📌 Build e Installazione di PyLucene**

    Questo script automatizza il processo di **installazione di PyLucene**.

    ```bash
    #!/bin/bash
    set -e

    # Verifica che Java sia installato
    if ! command -v java &> /dev/null; then
        echo "Java non è installato. Installalo prima di procedere."
        exit 1
    fi

    # Configurazione delle variabili di ambiente per Java
    JAVA_BIN=$(which java)
    JAVA_HOME=$(dirname $(dirname $(readlink -f $JAVA_BIN)))
    export JCC_JDK=$JAVA_HOME
    export JCC_INCLUDES="$JAVA_HOME/include:$JAVA_HOME/include/linux"
    export JCC_LFLAGS="-L$JAVA_HOME/lib/server -ljvm"

    # Verifica che Python sia installato
    if ! command -v python3 &> /dev/null; then
        echo "Python3 non è installato. Installalo prima di procedere."
        exit 1
    fi

    # Configurazione delle variabili di ambiente per Python
    PYTHON_BIN=$(which python3)
    PREFIX_PYTHON=$(dirname $(dirname $(readlink -f $PYTHON_BIN)))
    export PYTHON="${PREFIX_PYTHON}/bin/python3"
    export JCC="${PYTHON} -m jcc"
    export NUM_FILES=16

    export LD_LIBRARY_PATH="$JAVA_HOME/lib/server:$LD_LIBRARY_PATH"

    # Scaricare e installare PyLucene
    echo "Scaricando PyLucene..."
    curl -s https://downloads.apache.org/lucene/pylucene/pylucene-9.4.1-src.tar.gz | tar -xz

    cd pylucene-9.4.1

    echo "Compilando JCC..."
    cd jcc
    $PYTHON setup.py build
    $PYTHON setup.py install
    cd ..

    echo "Compilando PyLucene..."
    make

    echo "Installando PyLucene..."
    make install

    echo "Installazione completata con successo!"
    ```

- **📌 Rendere Permanenti le Variabili d'Ambiente**

    Una volta completata l'installazione, potrebbe essere utile **rendere permanenti le variabili d'ambiente** aggiungendole automaticamente al file `.bashrc`. Il seguente script automatizza questo processo.

    ```bash
    #!/bin/bash

    ENV_VARS="
    
    # Variabili per Java
    export JAVA_BIN=\$(which java)
    export JAVA_HOME=\$(dirname \$(dirname \$(readlink -f \$JAVA_BIN)))
    export JCC_JDK=\$JAVA_HOME
    export JCC_INCLUDES=\$JAVA_HOME/include:\$JAVA_HOME/include/linux
    export JCC_LFLAGS=\"-L\$JAVA_HOME/lib/server -ljvm\"

    # Variabili per Python
    export PYTHON_BIN=\$(which python3)
    export PREFIX_PYTHON=\$(dirname \$(dirname \$(readlink -f \$PYTHON_BIN)))
    export PYTHON=\$PREFIX_PYTHON/bin/python3
    export JCC=\"\$PYTHON -m jcc\"

    # Percorso delle librerie Java
    export LD_LIBRARY_PATH=\"\$JAVA_HOME/lib/server:\$LD_LIBRARY_PATH\"
    "

    BASHRC_FILE="$HOME/.bashrc"

    # Verifica se le variabili sono già presenti nel file
    if ! grep -Fxq "$ENV_VARS" "$BASHRC_FILE"; then
        echo -e "$ENV_VARS" >> "$BASHRC_FILE"
    fi

    source "$BASHRC_FILE"
    ```

- **📌 Verifica dell'installazione**

    Per verificare che l'installazione di PyLucene sia andata a buon fine, esegui il seguente comando. Se non ci sono errori, l'installazione è stata completata correttamente:

    ```bash
    python -c "import lucene; lucene.initVM()"
    ```

<br />

## Collaboratori

**Matteo Menozzi** $-$ (*Tremors3*) vedi [pagina](https://github.com/Tremors3) GitHub.

**Gabriele Turci** $-$ (*HerryTS*) vedi [pagina](https://github.com/HerryTS) GitHub.

**Enrico Turci Sologni** $-$ (*Gabeee88*) vedi [pagina](https://github.com/Gabeee88) GitHub.

**Andrei Dobrovolski** $-$ (*ADobrovolski*) vedi [pagina](https://github.com/ADobrovolski) GitHub.

<br />