#!/usr/bin/env python3

import psycopg as psy
from Setup.Utils import dbname, user, password
from Setup.tasks import task1, task2, task3, task4 
import pandas as pd


def main():
    connection = psy.connect(
    host="localhost",
    dbname=dbname,
    user=user,
    password=password,
    port=5432
    )
    cursor = connection.cursor()

    querys =["""SELECT name, title
                FROM Auth, Publ
                WHERE Auth.pubID = Publ.pubID;""",
             """SELECT title
                FROM Auth , Publ
                WHERE Auth . pubID = Publ . pubID AND 
                Auth . name = 'Divesh Srivastava' """]

    all_results = []
    all_results += task1(cursor, querys)
    all_results += task2(cursor, querys)
    all_results += task3(cursor, querys)
    all_results += task4(cursor, querys)

    connection.commit()
    cursor.close()
    connection.close()

    df = pd.DataFrame(all_results)
    print("\nFinal Summary Table:\n")
    print(df.to_markdown())
    
    df.to_csv("join_strategy_results.csv", index=False)

if __name__ == "__main__":
    main()
