#!/usr/bin/env python3
import psycopg as psy
from Utils import dbSetup, use_sqlite3


connection = dbSetup()
cursor = connection.cursor()
print("Your data is loading this may take a while...")
# NAIVE APPROACH 
''' The Naive Approach is to load every tuble with a extra INSERT statement
    The single statements dont get pre compiled or anything.
    We still establishing only one time a connection instead to establish a connetcion
    for every single statement.'''
tupleLimit = 10000
def insert_auth_data(file_path):
    with open(file_path, 'r') as file:
        next(file)  # Skip header row
        count = 0
        for line in file:
            if count >= tupleLimit:
                break
            columns = line.strip().split('\t')  # Split by tab
            name = columns[0]
            pubID = columns[1]
            insert_query = "INSERT INTO Auth (name, pubID) VALUES "
            if use_sqlite3:
                insert_query += "(?, ?);"
            else:
                insert_query += "(%s, %s);"
            cursor.execute(insert_query, (name, pubID))
            count +=1
            connection.commit()
   
def insert_publ_data(file_path):
    with open(file_path, 'r') as file:
        next(file)  # skips header 
        count = 0
        for line in file:
            if count >= tupleLimit: # load only first 1000 entrys
                break

            columns = line.strip().split('\t')
            
            if len(columns) < 5: # if a whole attribute is missing 
                print(f"Not enough columns(zu wenig Spalten): {columns}")
                continue  # Diese Zeile überspringen
            
            while len(columns) < 6: #if publisher is unknown : replace "" with "unknown"
                columns.append("Unknown")

            pubID, type_, title, booktitle, year, publisher = columns
            insert_query = """
            INSERT INTO Publ (pubID, type, title, booktitle, year, publisher)
            """
            if use_sqlite3:
                insert_query += "VALUES (?, ?, ?, ?, ?, ?);"
            else:
                insert_query += "VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_query, (pubID, type_, title, booktitle, year, publisher))
            count += 1
            connection.commit() # Naive approach comitted after every line
    
# Load data from auth.tsv and publ.tsv
filepath1 = 'auth.tsv'
filepath2 = 'publ.tsv'
insert_auth_data(filepath1)
insert_publ_data(filepath2)  
cursor.close()
connection.close()
print(f"Data loading complete for {filepath1} & {filepath2}. ~Naive.py")


