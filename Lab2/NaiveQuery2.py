#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, user, password, printQueryResults


def make_naive_query2(connection):
    try:
        cursor = connection.cursor() 
        query = """
        SELECT ssnum
        FROM Employee
        WHERE dept IN (SELECT dept FROM Techdept)        """
        cursor.execute(query)
        #printQueryResults(cursor, result_limit = 100)
    except Exception: 
        raise 
    finally:
        cursor.close()
        connection.close()


def main():
    connection = dbSetup(dbname, user, password)
    make_naive_query2(connection)


if __name__ == "__main__":
    main()
