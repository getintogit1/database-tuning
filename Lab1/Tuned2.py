#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbname, user, password 

'''    Using COPY instead of INSERT
    Every INSERT runs as a separate transaction (unless batched), which involves disk writes and logging.
    COPY bypasses this by writing data in large chunks, reducing overhead.   
    COPY writes data in binary or CSV mode, reducing I/O operations.
    INSERT executes multiple smaller disk writes, making it slower.
    Indexing impact (If the table has many indexes, inserting in batches may be beneficial).'''

tuplelimit = 10000
def optimize_db(cursor):
    print("Increasing work memory and diasble WAL logging temporarily...")
    cursor.execute(f"GRANT pg_read_server_files TO {user}")
    cursor.execute("ALTER TABLE publ SET UNLOGGED;")                            # Disable WAL logging
    cursor.execute("SET work_mem = '4GB';")                                     # Increase work_mem temporarily

def restore_db(cursor):
    print("Restoring database settings after data loading...")
    cursor.execute("ALTER TABLE publ SET LOGGED;")  # Enable WAL logging
    cursor.execute("RESET work_mem;")  # Reset work_mem to default

def copy_publ_data(file_path, cursor):
    with open(file_path, 'r') as file:
        next(file)  # Skip the header row
        cursor.copy_from(file, 'publ', sep='\t', columns=(
            'pubid', 'type', 'title', 'booktitle', 'year', 'publisher'))

def copy_auth_data(file_path, cursor):                                          #cursor.copy_from() requires PostgreSQL superuser privileges.    with ope
    with open(file_path, 'r') as file:
        next(file)  # Skip header row
        cursor.copy_from(file, 'auth', sep='\t', columns=('name', 'pubid'))


def main():
    connection = psy.connect(
        host="localhost", 
        dbname=dbname, 
        user=user, 
        password=password, 
        port=5432
    )
    cursor = connection.cursor()
    print("Your data is loading this may take a while...")
    optimize_db(cursor)
    authData = "auth.tsv"
    publData = "publ.tsv"
    copy_auth_data(authData, cursor)
    copy_publ_data(publData, cursor)
    restore_db(cursor)
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data loading complete for {authData} & {publData}. ~Tuned2.py")

if __name__ == "__main__":
    main()
