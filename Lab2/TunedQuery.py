#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, printQueryResults, user, password




def make_tuned_query(connection):
    try:
        cursor = connection.cursor() 
        query = """
            SELECT Employee.ssnum
            FROM Employee, Student
            WHERE Employee.ssnum = Student.ssnum;
        """
        cursor.execute(query)
        printQueryResults(cursor, result_limit = 100)
    except Exception: 
        raise 
    finally:
        cursor.close()
        connection.close()


def main():
    connection = dbSetup(dbname, user, password)
    make_tuned_query(connection)


if __name__ == "__main__":
    main()
