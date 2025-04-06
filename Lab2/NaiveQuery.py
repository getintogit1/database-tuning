#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, user, password, printQueryResults


def make_naive_query(connection):
    try:
        cursor = connection.cursor() 
        query = """
        SELECT distinct E1.ssnum
        FROM Employee E1, Techdept T
        WHERE E1.salary between ((SELECT AVG(E2.salary)
        FROM Employee E2, Techdept T
        WHERE E2.dept = E1.dept
        AND E2.dept = T.dept) - 1000) and ((SELECT AVG(E2.salary)
        FROM Employee E2, Techdept T
        WHERE E2.dept = E1.dept
        AND E2.dept = T.dept) + 1000);        """
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
