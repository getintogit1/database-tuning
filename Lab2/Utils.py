#!/usr/bin/env python3
import psycopg2 as psy
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


def dbSetup(dbname, user, password):
    
    
    connection = psy.connect(
    host="localhost", 
    dbname=dbname, 
    user=user, 
    password=password, 
    port= 5432)
   
    print(f"""You created a connection with following informations:
    host="localhost", 
    dbname={dbname}, 
    user={user}, 
    password={password}, 
    port= 5432""")
    return connection

dbname, user, password = credentials()

def printQueryResults(cursor, result_limit):
        counter = 0
        results = cursor.fetchall()
        print("Results of Query:")
        for row in results:
            if counter >= result_limit:
                break
            print(row)
            counter += 1

    
