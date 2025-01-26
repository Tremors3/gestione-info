# NUOVO METODO

SO: Arch Linux
Java Version: 21.0.6
Python Version: 3.13.1
PyLucene Version: 10.0.0

## Installazione di PyLucene

Segui questi passaggi per scaricare e installare PyLucene 10.0.0 .

### **1. Scaricare l'installer di PyLucene**

Inizia clonando il repository di PyLucene dall'AUR:

```bash
# Clona il repository di PyLucene
git clone https://aur.archlinux.org/packages/pylucene
cd pylucene
```

### **2. Installare la dipendenza necessaria**

Installare la dipendenza python necessaria; il pacchetto "`setuptools`" contiene la dipendenza "`distutils`" necessaria che è stata deprecata:

```bash
# Installa la dipendenza
pacman -Syu python-setuptools
```

### **2. Compilare PyLucene e risolvere l'errore**

Builda per la prima volta pylucene e aspetta di ricevere un errore dopo più o meno 5 minuti.

```bash
# Entra nella cartella scaricata in precedenza
cd pylucene
# Compila e installa PyLucene
makepkg -sric
```

L'errore è il seguente:

"`cp: cannot stat 'build/lib.linux-x86_64-cpython-312/*': no such file or directory`"

Per risolverlo:

1) Recarsi al seguente percorso all'interno della cartella "pylucene/":

```bash
cp src/pylucene-10.0.0/build/
```

2) Rinominare i seguenti file come mostrato:

```bash
cp -r lib.linux-x86_64-cpython-313 lib.linux-x86_64-cpython-312
cp -r temp.linux-x86_64-cpython-313 temp.linux-x86_64-cpython-312
```

3) Non fare domande.

4) Rieffettuare la build ritornando alla cartella "pylucene/"

```bash
# Entra nella cartella scaricata in precedenza
cd pylucene
# Compila e installa PyLucene
makepkg -sric
```

Il processo richiederà circa 5 minuti e potrebbe richiedere l'inserimento della password in alcuni momenti.




















# VECCHIO METODO (NON FUNZIONA, NON SEGUIRMI)

LA BUILD E' STATA MODIFICATA QUINDI QUESTO METODO NON E' PIU' REALIZZABILE!

# Installazione di PyLucene su Arch Linux

Segui questi passaggi per scaricare e installare PyLucene 10.0.0.

### **1. Scaricare l'installer di PyLucene**

Inizia clonando il repository di PyLucene dall'AUR:

```bash
# Clona il repository di PyLucene
git clone https://aur.archlinux.org/packages/pylucene
cd pylucene
```

### **2. Modificare il PKGBUILD**

All'interno della cartella `pylucene`, apri il file `PKGBUILD` per modificare la versione e il checksum. Controlla la versione e il SHA256 sul [sito ufficiale](https://dlcdn.apache.org/lucene/pylucene/) di Apache Lucene:

- **Versione**: pylucene-10.0.0-src.tar.gz
- **SHA256**: Puoi trovare il checksum sul sito di Apache [qui](https://dlcdn.apache.org/lucene/pylucene/pylucene-10.0.0-src.tar.gz.sha256).

Modifica il file `PKGBUILD`:

```bash
# Apri il file PKGBUILD con un editor di testo
vim PKGBUILD
```

Cambia le seguenti righe:

```bash
pkgver=10.0.0
sha256sums=(...)  # Sostituisci i puntini con il checksum SHA256
```

Salva e chiudi il file.

### **3. Installare la versione corretta di Java**

Per PyLucene 10.0.0, puoi utilizzare Java 21 o Java 23. In questo esempio, installeremo Java 23:

```bash
# Installa JDK OpenJDK
sudo pacman -S jdk-openjdk

# Seleziona Java 23 come versione predefinita
sudo archlinux-java set java-23-openjdk

# Verifica la selezione
archlinux-java status
```

### **4. Compilare e installare PyLucene**

Ora sei pronto per compilare e installare PyLucene. Il processo richiederà circa 5 minuti e potrebbe richiedere l'inserimento della password in alcuni momenti:

```bash
# Compila e installa PyLucene
makepkg -sri
```

### **5. Risolvere l'errore `libjvm.so` mancante**

Se ricevi un errore riguardo alla libreria `libjvm.so` quando provi a importare lucene, puoi risolverlo aggiungendo il percorso della libreria al tuo LD_LIBRARY_PATH:

1. **Trovare il percorso di libjvm.so**

    Per identificare il percorso del file `libjvm.so`, puoi utilizzare il comando `find`. Questo comando cercherà in tutte le directory di JDK installate per trovare il file specificato:

    ```bash
    # Cerca il file libjvm.so nelle directory JDK
    find /usr/lib/jvm -name "libjvm.so"
    ```

    Output atteso:

    ```bash
    /usr/lib/jvm/java-XX-openjdk/lib/server
    ```

    Sostituisci `XX` con la versione specifica di OpenJDK installata sul tuo sistema.

2. **Aggiungere il percorso a LD_LIBRARY_PATH**

    Una volta ottenuto il percorso corretto, aggiungilo alla variabile d'ambiente `LD_LIBRARY_PATH`. Questo permette al sistema di trovare `libjvm.so` quando cerchi di importare moduli che dipendono da essa.

    ```bash
    # Aggiungi il percorso di libjvm.so alla variabile d'ambiente LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jvm/java-23-openjdk/lib/server
    ```

    Per rendere questa modifica permanente, puoi aggiungere la riga al tuo file `.bashrc` o `.bash_profile`.