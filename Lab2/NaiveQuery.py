#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, user, password, printQueryResults


def make_naive_query(connection):
    try:
        cursor = connection.cursor() 
        query = """
        SELECT Employee.ssnum
        FROM Employee, Student
        WHERE Employee.name = Student.name;        """
        cursor.execute(query)
        #printQueryResults(cursor, result_limit = 100)
    except Exception: 
        raise 
    finally:
        cursor.close()
        connection.close()


def main():
    connection = dbSetup(dbname, user, password)
    make_naive_query(connection)


if __name__ == "__main__":
    main()
