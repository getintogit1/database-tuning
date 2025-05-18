#!/usr/bin/env python3

import psycopg as psy
from Setup.Utils import dbname, user, password

def get_unique_values(cursor, column, limit=75):
    query = f"SELECT {column} FROM publ WHERE {column} IS NOT NULL GROUP BY {column} ORDER BY RANDOM() LIMIT %s;"
    cursor.execute(query, (limit,))
    return [row[0] for row in cursor.fetchall()]

connection = psy.connect(
    host="localhost",
    dbname=dbname,
    user=user,
    password=password,
    port=5432
)
cursor = connection.cursor()

pubids = get_unique_values(cursor, 'pubID')         
booktitles = get_unique_values(cursor, 'booktitle') 
years = get_unique_values(cursor, 'year')          

cursor.close()
connection.close()
