#!/usr/bin/env python3
import psycopg as psy
import sqlite3
import sys
import Utils

def createTables(connection):
    cursor = connection.cursor() 
    cursor.execute("""
    CREATE TABLE Auth (
        name VARCHAR(49),
        pubID VARCHAR(129)
        );""")

    cursor.execute("""
    CREATE TABLE Publ (
        pubID VARCHAR(129),
        type VARCHAR(13),
        title VARCHAR(700),
        booktitle VARCHAR(132),
        year VARCHAR(4),
        publisher VARCHAR(196)
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()

    print("Created Table Auth and Publ complete.")

def main():
    connection = Utils.dbSetup()
    createTables(connection)

Utils.use_sqlite3 = False
main()
Utils.use_sqlite3 = True
main()
