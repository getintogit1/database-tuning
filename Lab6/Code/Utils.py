#!/usr/bin/env python3
import sys
import psycopg as psy
import sqlite3
import json
import argparse
import os

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


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--numthreads', type=int, default=1)
    parser.add_argument('-c', '--maxconcurrent', type=int, default=1)
    parser.add_argument('-i', '--isolation', choices=['read_committed', 'serializable'], default='read_committed')
    parser.add_argument('-s', '--solution', choices=['a', 'b'], default= 'a')
    args = parser.parse_args()
    return args


def write_csv(args, maxconcurrent, correctness, duration):
    write_header = not os.path.exists("results.csv")
    with open("results.csv", "a") as f:
        if write_header:
            f.write("isolation,maxconcurrent,correctness,duration\n")
        f.write(f"{args.isolation},{maxconcurrent},{correctness},{duration:.4f}\n")
