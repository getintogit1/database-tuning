#!/usr/bin/env python3

import psycopg as psy
import time
from Setup.Utils import dbname, user, password, explain_query


def dropOldIndex(cursor):
    cursor.execute("DROP INDEX IF EXISTS idx_publ_pubid_nonclustered;")
    cursor.execute("DROP INDEX IF EXISTS idx_publ_pubid_clustered;")
    cursor.execute("DROP INDEX IF EXISTS idx_auth_pubid_clustered;")


def createNonClusteredBTree(table, column):
    def create(cursor):
        print(f"Creating non-clustered index on {table}.{column}")
        cursor.execute(f"CREATE INDEX idx_publ_pubid_nonclustered ON {table} ({column});")
    return create


def createClusteredBTree(table, column):
    def create(cursor):
        print(f"Creating clustered index on {table}.{column}")
        cursor.execute(f"CREATE INDEX idx_{table.lower()}_{column.lower()}_clustered ON {table} ({column});")
        cursor.execute(f"CLUSTER {table} USING idx_{table.lower()}_{column.lower()}_clustered;")
    return create


def run_query_with_timing(cursor, query):
    cursor.execute("DISCARD ALL;")  
    start = time.time()
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    output = cursor.fetchall()
    duration = time.time() - start
    return duration, "\n".join([line[0] for line in output])


def run_experiment(cursor, index_creators, query):
    if index_creators is None or index_creators == [None]:
        name = "No Index"
        index_creators = []  
    else:
        name = ", ".join(f"{fn.__name__}" for fn in index_creators)

    print(f"\n=== Running experiment: {name} ===")
    dropOldIndex(cursor)

    for creator in index_creators:
        creator(cursor)

    duration, plan = run_query_with_timing(cursor, query)
    print(plan)
    print(f"Execution time for '{name}': {duration:.4f} seconds\n")
    return {"name": name, "plan": plan, "time": duration}


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
    
    for query in querys:
        run_experiment(cursor,[None], query)
        run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID")], query)
        run_experiment(cursor, [createClusteredBTree("Publ", "pubID"), createClusteredBTree("Auth", "pubID")], query)
    
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
