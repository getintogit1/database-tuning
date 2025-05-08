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

def dropOldIndex(cursor):
    cursor.execute("DROP INDEX IF EXISTS idx_pubid_clustered, idx_booktitle, idx_year, idx_pubid_nonClustered, idx_pubid_hash;")

def createClusteredBTree(cursor):
    cursor.execute("CREATE INDEX idx_pubid_clustered ON Publ(pubID);")
    cursor.execute("CLUSTER Publ USING idx_pubid_clustered;")  # Sorts table once

def createNonClusteredBTree(cursor):
    cursor.execute("CREATE INDEX idx_pubid_nonClustered ON Publ(pubID);")

def createHashIndex(cursor):
    cursor.execute("CREATE INDEX idx_pubid_hash ON Publ USING hash(pubID);")


def explain_query(cursor, query, params):
    cursor.execute("EXPLAIN ANALYZE " + query, params)
    plan = cursor.fetchall()
    print("\n".join(row[0] for row in plan))
