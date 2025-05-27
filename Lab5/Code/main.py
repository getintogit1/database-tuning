#!/usr/bin/env python3

import psycopg as psy
from Setup.Utils import dbname, user, password
from Setup.tasks import task1, task2, task3, task4 


def main():
    connection = psy.connect(
    host="localhost",
    dbname=dbname,
    user=user,
    password=password,
    port=5432
    )
    connection.autocommit = True  
    cursor = connection.cursor()

    querys =["""SELECT name, title
                FROM Auth, Publ
                WHERE Auth.pubID = Publ.pubID;""",
             """SELECT title
                FROM Auth , Publ
                WHERE Auth . pubID = Publ . pubID AND 
                Auth . name = 'Divesh Srivastava' """]

    task1(cursor, querys)
    task2(cursor, querys)
    task3(cursor, querys)
    task4(cursor, querys)

    connection.commit()
    cursor.close()
    connection.close()
    

if __name__ == "__main__":
    main()
