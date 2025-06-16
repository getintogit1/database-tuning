#!/bin/bash

set -e

DB_USER="sam"
DB_NAME="tuninglab6"

echo "===== Creating database if not exists ====="
createdb -U $DB_USER $DB_NAME || echo "Database $DB_NAME already exists."

echo "===== Creating the Accounts table ====="
psql -U $DB_USER -d $DB_NAME -f create_accountDB.sql || echo "Table already exists!"

echo "===== Solution A: Running main.py READ COMMITTED (workers 1-5) ====="
for c in 1 2 3 4 5
do
    echo "----- Running Solution with $c concurrent workers (READ COMMITTED) -----"
    python3 main.py -t 100 -c $c -i read_committed -s a
done

echo "===== Solution A: Running main.py SERIALIZABLE (workers 1-5) ====="
for c in 1 2 3 4 5
do
    echo "----- Running with $c concurrent workers (SERIALIZABLE) -----"
    python3 main.py -t 100 -c $c -i serializable -s a
done

echo "===== Solution B: Running main.py READ COMMITTED (workers 1-5) ====="
for c in 1 2 3 4 5
do
    echo "----- Running Solution with $c concurrent workers (READ COMMITTED) -----"
    python3 main.py -t 100 -c $c -i read_committed -s b
done

echo "===== Solution B: Running main.py SERIALIZABLE (workers 1-5) ====="
for c in 1 2 3 4 5
do
    echo "----- Running with $c concurrent workers (SERIALIZABLE) -----"
    python3 main.py -t 100 -c $c -i serializable -s b
done

echo "===== DONE ====="

