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