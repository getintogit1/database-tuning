#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, user, password

connection = dbSetup(dbname, user, password)
def createTables(connection):
    cursor = connection.cursor() 
    cursor.execute("""
    CREATE TABLE Auth (
        name VARCHAR(49),
        pubID VARCHAR(129)
        );

    CREATE TABLE Publ (
        pubID VARCHAR(129),
        type VARCHAR(13),
        title VARCHAR(700),
        booktitle VARCHAR(132),
        year SMALLINT(4),
        publisher VARCHAR(196)
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()

    print("Created Table Auth and Publ complete.")

createTables(connection)
