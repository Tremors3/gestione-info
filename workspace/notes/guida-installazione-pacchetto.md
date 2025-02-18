# Premesse

Questo tutorial descrive il processo di installazione della mia applicazione su **Ubuntu in WSL2** (Windows 11). I passaggi illustrati sono ottimizzati per questo ambiente, ma possono essere adattati anche a sistemi **Ubuntu** o **Debian** nativi, con alcune variazioni.

### Compatibilità con ambienti virtualizzati

Si **sconsiglia** di eseguire il tutorial su macchine virtuali gestite da **VirtualBox** o **VMware**, poiché l'installazione di Docker richiede **KVM Nested Virtualization**, una funzionalità non supportata da tutti gli hypervisor.

### Opzioni consigliate:

- **Ubuntu/Debian su WSL2** (Windows 11) $\rightarrow$ *Supporta KVM Nested Virtualization ed è la scelta raccomandata*.
- **Ubuntu/Debian installati direttamente su hardware fisico** $\rightarrow$ *Alternativa valida se non si usa WSL2*.

Se state utilizzando un hypervisor che non supporta la **KVM Nested Virtualizaiton**, l'installazione di Docker potrebbe non funzionare correttamente.






# Installazione di WSL2 e Ubuntu

Questa sezione guida nell'abilitazione di **WSL2** su Windows 11 e nell'installazione di **Ubuntu**.

1) Abilitare e installare WSL2

    Aprire il **Prompt dei comandi** o **PowerShell** come amministratore e digitare i seguenti comandi per installare WSL e Ubuntu:

    ```powershell
    wsl --install
    wsl --install -d Ubuntu
    # Il primo comando abilita WSL2, mentre il secondo installa Ubuntu come distribuzione predefinita.
    ```

1) Primo avvio di Ubuntu

    Una volta completata l'installazione, avviare Ubuntu digitando:

    ```powershell
    wsl
    ```

    Al primo avvio, verrà richiesto di **creare un utente** e impostare una **password**.
    Dopo l'accesso alla shell, è consigliato aggiornare i mirror dei pacchetti con:

    ```
    sudo apt update
    ```






# Installazione del servizio Docker

Questa sezione guida nell'installazione di **Docker** su WSL2 e nella configurazione di **KVM Nested Virtualization**, necessaria per il corretto funzionamento di Docker in questo ambiente.

**Nota**: Se stai utilizzando **Ubuntu/Debian con Docker già installato e funzionante**, puoi saltare questa fase.

1) **Abilitare KVM Nested Virtualization**

    WSL2 supporta la **Nested Virtualization**, ma questa opzione non è abilitata di default. Per attivarla, segui questi passaggi:

    **Installare i pacchetti necessari**

    Eseguire il seguente comando per installare i pacchetti richiesti da KVM:

    ```bash
    sudo apt install qemu-system-x86 libvirt-daemon-system virtinst \
        virt-manager virt-viewer ovmf swtpm qemu-utils guestfs-tools \
        libosinfo-bin tuned cpu-checker
    ```

    **Aggiungere l'utente al gruppo KVM**

    ```bash
    sudo usermod -a -G kvm ${USER}
    ```
    - *Dopo aver eseguito questo comando, potrebbe essere necessario disconnettersi e riconnettersi affinché le modifiche abbiano effetto*.

    **Modificare i permessi di /dev/kvm**

    Per rendere i permessi permanenti, aggiungere queste righe al file **/etc/wsl.conf**:

    ```bash
    [boot]
    command = /bin/bash -c 'chown -v root:kvm /dev/kvm && chmod 660 /dev/kvm'
    ```

    **Abilitare Nested Virtualization in WSL2**

    Aggiungere questa configurazione sempre nel file **/etc/wsl.conf**:

    ```bash
    [wsl2]
    nestedVirtualization=true
    ```

    **Riavviare WSL**

    Per applicare le modifiche, riavviare WSL eseguendo in PowerShell o nel Prompt dei comandi:

    ```powershell
    wsl --shutdown
    ```

    Una volta riavviato, **WSL2 avrà la Nested Virtualization attivata**.

2) **Verificare il supporto KVM**

    Per caricare manualmente il modulo KVM, eseguire:

    ```bash
    sudo modprobe kvm
    ```

    Se si utilizza un **processore Intel** o **AMD**, eseguire uno dei seguenti comandi:

    ```bash
    sudo modprobe kvm_intel  # Per processori Intel
    sudo modprobe kvm_amd    # Per processori AMD
    ```

    Verificare che **KVM sia attivo** con:

    ```bash
    kvm-ok
    ```

    Se il comando restituisce "**KVM acceleration can be used**", la configurazione è avvenuta con successo.

3) **Installazione e Abilitazione di Docker**

    Prima di installare Docker Engine per la prima volta su un nuovo sistema, è necessario configurare il repository **apt** ufficiale di Docker. Successivamente, Docker potrà essere installato e aggiornato direttamente da questo repository.

    **Riferimento ufficiale**: [Installazione di Docker su Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

    1) Configurare il repository apt di Docker

        Eseguire i seguenti comandi per aggiungere il repository ufficiale di Docker:

        ```bash
        # Add Docker official GPG key:
        sudo apt-get update
        sudo apt-get install ca-certificates curl
        sudo install -m 0755 -d /etc/apt/keyrings
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        sudo chmod a+r /etc/apt/keyrings/docker.asc

        # Add the repository to Apt sources:
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
          $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        ```

    2) Installare Docker

        Ora è possibile installare Docker eseguendo:

        ```bash
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```

    3) Verificare l'installazione

        ```bash
        sudo docker run hello-world
        ```

        - *Questo comando scarica un'immagine di test e la esegue in un container. Se l'installazione è avvenuta con successo, verrà mostrato un messaggio di conferma.*











# Installazione Conda su WSL2

1. Scaricare e installare Anaconda

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
    4. **Quando viene chiesto di inizializzare Conda**, digitare `yes`.

2. Abilitare Conda nella sessione

    Dopo l'installazione, attivare Conda ed eseguire l'inizializzazione:

    ```bash
    source ~/.bashrc
    conda init
    ```

3. Creare l'ambiente dedicato a PyLucene
    
    Creare un nuovo ambiente virtuale chiamato `lucene` con Python:

    ```bash
    conda create -n lucene python=3.12
    ```

    Attivare l'ambiente:

    ```bash
    conda activate lucene
    ```

    Ogni volta che apri una nuova sessione della shell, dovrai riattivare l'ambiente eseguendo nuovamente questo comando.











# Installazione PyLucene

Questo script automatizza l'**installazione di PyLucene**. Si consiglia di eseguirlo all'interno di un **ambiente Conda dedicato** per garantire una gestione ottimale delle dipendenze.

```bash
#!/bin/bash
set -e  # Interrompe lo script in caso di errore

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

Dopo aver completato l'installazione, potrebbe essere utile **rendere permanenti le variabili d'ambiente** aggiungendole automaticamente al file `.bashrc`. Il seguente script automatizza il processo.

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
export NUM_FILES=16

# Percorso delle librerie Java
export LD_LIBRARY_PATH=\"\$JAVA_HOME/lib/server:\$LD_LIBRARY_PATH\"
"

BASHRC_FILE="$HOME/.bashrc"

# Verifica se le variabili sono già presenti nel file
if ! grep -Fxq "$ENV_VARS" "$BASHRC_FILE"; then
    echo "$ENV_VARS" >> "$BASHRC_FILE"
fi

source "$BASHRC_FILE"
```









### 👉 Installazione Pacchetto

Per installare il pacchetto, utilizzeremo `pip`. È consigliabile eseguire l'installazione all'interno di un ambiente virtuale Python, gestito ad esempio tramite **Conda** (lo stesso ambiente in cui è installato PyLucene).

- **📌 Clonare il repository GitHub:**
    
    ```bash
    git clone https://github.com/Tremors3/gestione-info.git
    ```

- **📌 Navigare nella cartella del progetto e installare il pacchetto:**

    ```bash
    cd gestione-info
    pip install .
    ```

- **📌 Inizializzare l'applicazione con il seguente comando:**

    ```bash
    graboidrfc --install
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