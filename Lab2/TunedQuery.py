#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, printQueryResults, user, password
import Utils



def make_tuned_query(connection):
    try:
        cursor = connection.cursor() 
        avg_salary_query = """
        SELECT AVG(E.salary)
        FROM Employee E
        JOIN Techdept T ON E.dept = T.dept
        """
        cursor.execute(avg_salary_query)
        avg_salary = cursor.fetchone()[0]

        query = """
        SELECT DISTINCT E.ssnum
        FROM Employee E
        JOIN Techdept T ON E.dept = T.dept
        """
        if Utils.use_sqlite3:
            query += " WHERE E.salary BETWEEN ? AND ?"
        else:
            query += " WHERE E.salary BETWEEN %s AND %s"
        lower_bound = avg_salary - 1000
        upper_bound = avg_salary + 1000

        cursor.execute(query, (lower_bound, upper_bound))

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
