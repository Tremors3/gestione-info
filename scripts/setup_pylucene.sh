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
export JCC_LFLAGS="-L$JAVA_HOME/lib/server:-ljvm"

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
echo "Scaricamento PyLucene..."
curl -s https://downloads.apache.org/lucene/pylucene/pylucene-9.4.1-src.tar.gz | tar -xz

cd pylucene-9.4.1

echo "Compilazione JCC..."
cd jcc
$PYTHON setup.py build
$PYTHON setup.py install
cd ..

echo "Compilazione PyLucene..."
make

echo "Installazione PyLucene..."
make install

echo "Installazione completata con successo!"