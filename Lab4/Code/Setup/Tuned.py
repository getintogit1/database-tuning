#!/usr/bin/env python3
import psycopg as psy
import os
from Utils import use_sqlite3, dbSetup


connection = dbSetup()
cursor = connection.cursor()
print("Your data is loading this may take a while...")

tupleLimit = 100000000

def insert_auth_data(file_path, batch_size=1000):
    count = 0
    batch = []
    
    with open(file_path, 'r', encoding="utf-8") as file:
        next(file)  # Skip header row
        for line in file:
            if count >= tupleLimit:
                break
            columns = line.strip().split('\t')  
            name = columns[0]
            pubID = columns[1]
            batch.append((name, pubID))
            if len(batch) >= batch_size:
                execute_batch(batch)
                batch = []  # Reset batch after execution
            count += 1
    if batch:
        execute_batch(batch)


def execute_batch(batch):
    if use_sqlite3:
        cursor.executemany("INSERT INTO Auth (name, pubID) VALUES (?, ?);", batch)
    else:
        placeholders = ', '.join(['(%s, %s)'] * len(batch))
        values = [item for sublist in batch for item in sublist]  # Flatten the batch list into a single list of values
        cursor.execute(f"INSERT INTO Auth (name, pubID) VALUES {placeholders};", values)


def insert_publ_data(file_path, batch_size=1000):
    count = 0
    batch = []
    
    with open(file_path, 'r', encoding="utf-8") as file:
        next(file)  # Skip the header row
        for line in file:
            if count >= tupleLimit:
                break
            columns = line.strip().split('\t')
            if len(columns) < 5: # if a whole attribute is missing 
                columns += [""] * (6 - len(columns))  # Fill missing columns            
            while len(columns) < 6: #if publisher is unknown : replace "" with "unknown"
                columns.append("Unknown")            
            pubID, type_, title, booktitle, year, publisher = columns
            batch.append((pubID, type_, title, booktitle, year, publisher))
            if len(batch) >= batch_size:
                execute_batch_publ(batch)
                batch = []  # Reset batch after execution
            count += 1
    if batch:
        execute_batch_publ(batch)


def execute_batch_publ(batch):
    if use_sqlite3:
        cursor.executemany("INSERT INTO Publ (pubID, type, title, booktitle, year, publisher) VALUES (?, ?, ?, ?, ?, ?);", batch)
    else:
        placeholders = ', '.join(['(%s, %s, %s, %s, %s, %s)'] * len(batch))
        values = [item for sublist in batch for item in sublist]
        cursor.execute(f"INSERT INTO Publ (pubID, type, title, booktitle, year, publisher) VALUES {placeholders};", values, prepare = True)

base_path = os.path.dirname(os.path.abspath(__file__))
filepath1 = os.path.join(base_path, 'auth.tsv')
filepath2 = os.path.join(base_path, 'publ.tsv')
#filepath1 = 'auth.tsv'
#filepath2 = 'publ.tsv'
insert_auth_data(filepath1)
insert_publ_data(filepath2) 
connection.commit()
cursor.close()
connection.close()
print(f"Data loading complete for {filepath1} & {filepath2}. ~Tuned.py")


