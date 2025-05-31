#!/usr/bin/env python3
import sys
import psycopg as psy
import sqlite3
import json

def credentials():
    try:
        # Try to load credentials if they exist
        with open("db_credentials.json", "r") as file:
            creds = json.load(file)
            print("Using saved credentials.")
            return creds["dbname"], creds["user"], creds["password"]
    except (FileNotFoundError, json.JSONDecodeError):
        # Ask for credentials if no file is found
        print("Enter your PostgreSQL credentials (saved for future use).")
        dbname = input("Database name: ")
        user = input("User: ")
        password = input("Password: ")

        # Save credentials to a JSON file
        with open("db_credentials.json", "w") as file:
            json.dump({"dbname": dbname, "user": user, "password": password}, file)

        return dbname, user, password

use_sqlite3 = len(sys.argv) > 1 and sys.argv[1] == '--sqlite'
dbname, user, password = credentials()

def dbSetup():
    if use_sqlite3:
        connection = sqlite3.connect("db.sqlite")
        print("You created a SQLite connection at db.sqlite")
    else:
        connection = psy.connect(
        host="localhost", 
        dbname=dbname, 
        user=user, 
        password=password, 
        port= 5432)
       
        print(f"""You created a PostgreSQL connection with following informations:
        host="localhost", 
        dbname={dbname}, 
        user={user}, 
        password={password}, 
        port= 5432""")
    return connection

def explain_query(cursor, query):
    cursor.execute("EXPLAIN ANALYZE " + query)
    plan = cursor.fetchall()
    print("\n".join(row[0] for row in plan))


def dropOldIndex(cursor):
    cursor.execute("DROP INDEX IF EXISTS idx_publ_pubid_nonclustered;")
    cursor.execute("DROP INDEX IF EXISTS idx_auth_pubid_nonclustered;")
    cursor.execute("DROP INDEX IF EXISTS idx_publ_pubid_clustered;")
    cursor.execute("DROP INDEX IF EXISTS idx_auth_pubid_clustered;")


def createNonClusteredBTree(table, column):
    def createNonClustered(cursor):
        print(f"Creating non-clustered index on {table}.{column}")
        cursor.execute(f"CREATE INDEX idx_{table}_{column}_nonclustered ON {table} ({column});")
    return createNonClustered


def createClusteredBTree(table, column):
    def createClustered(cursor):
        print(f"Creating clustered index on {table}.{column}")
        cursor.execute(f"CREATE INDEX idx_{table.lower()}_{column.lower()}_clustered ON {table} ({column});")
        cursor.execute(f"CLUSTER {table} USING idx_{table.lower()}_{column.lower()}_clustered;")
    return createClustered


