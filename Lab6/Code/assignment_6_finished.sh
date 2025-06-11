#!/bin/bash

# Fail fast: Script stoppt bei Fehlern

#!/bin/bash

# Fail fast: Script stoppt bei Fehlern
set -e

# Konfiguration
DB_USER="sam"
DB_NAME="tuninglab6"

echo "===== STEP 0: Creating database if not exists ====="
# If database already exists, ignore error
createdb -U $DB_USER $DB_NAME || echo "Database $DB_NAME already exists."

echo "===== STEP 1: Creating the Accounts table ====="
psql -U $DB_USER -d $DB_NAME -f create_accountDB.sql || echo "Table already exists!"

echo "===== STEP 2: Running main.py READ COMMITTED (workers 1-5) ====="
for c in 1 2 3 4 5
do
    echo "----- Running with $c concurrent workers (READ COMMITTED) -----"
    python3 main.py -t 100 -c $c -i read_committed
done

echo "===== STEP 3: Running main.py SERIALIZABLE (workers 1-5) ====="
for c in 1 2 3 4 5
do
    echo "----- Running with $c concurrent workers (SERIALIZABLE) -----"
    python3 main.py -t 100 -c $c -i serializable
done

echo "===== DONE ====="

