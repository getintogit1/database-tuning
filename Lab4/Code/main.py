
#!/usr/bin/env python3
import psycopg as psy
import time
from Setup.Utils import (
    dbname, user, password , 
    dropOldIndex, createClusteredBTree, 
    createNonClusteredBTree, 
    createHashIndex, explain_query)


def run_and_time(cursor, query, params, repetitions=5):
    start = time.time()
    for _ in range(repetitions):
        cursor.execute(query, params)
        cursor.fetchall()  
    end = time.time()
    return (end - start) / repetitions  


def pointQuery(cursor):
    print("##### Point Query #####")
    query = "SELECT * FROM Publ WHERE pubID = %s;"
    explain_query(cursor, query, ('books/acm/kim95/Blakeley95',))  
    print("-" * 110)
    return run_and_time(cursor, query, ('books/acm/kim95/Blakeley95',))


def multiPointQuery(cursor):
    print("##### Multi Point #####")
    query = "SELECT * FROM Publ WHERE booktitle = %s;"
    explain_query(cursor, query, ('Modern Database Systems',))  
    print("-" * 110)
    return run_and_time(cursor, query, ('Modern Database Systems',))


def multiPointQueryInPredicate(cursor):
    print("##### Multipoint In Predict #####")
    query = "SELECT * FROM Publ WHERE pubID IN (%s);"
    explain_query(cursor, query, ('acm/kim95',))  
    print("-" * 110)
    return run_and_time(cursor, query, ('acm/kim95',))


def multiPointQueryHighSelectivity(cursor):
    print("##### High Selective Multipoint #####")
    query = "SELECT * FROM Publ WHERE year = %s;"
    explain_query(cursor, query, ('1944',))
    print("-" * 110)  
    return run_and_time(cursor, query, ('1944',))


def run_experiment(create_index_func):
    print(f"!!! ##### Running: {create_index_func} ##### !!!")
    connection = psy.connect(
        host="localhost",
        dbname=dbname,
        user=user,
        password=password,
        port=5432
    )
    cursor = connection.cursor()
    dropOldIndex(cursor)
    create_index_func(cursor)
    connection.commit()
    result = {
        "pointQuery":  pointQuery(cursor),
        "Multipoint": multiPointQuery(cursor),
        "Multipoint IN": multiPointQueryInPredicate(cursor),
        "High selectivity (year)": multiPointQueryHighSelectivity(cursor)
    }
    
    cursor.close()
    connection.close()
    return result





if __name__ == "__main__":
    result = {
            "Clustered BTree": run_experiment(createClusteredBTree),
            "Non Clustered BTree": run_experiment(createNonClusteredBTree),
            "Hash Index": run_experiment(createHashIndex),
            "Table Scan": run_experiment(lambda cursor: None)
    }
    query_types = ["pointQuery", "Multipoint", "Multipoint IN", "High selectivity (year)"]
    for query in query_types:
        min_time = float("inf")
        best_index = None
        for index_type, timings in result.items():
            if timings[query] < min_time:
                min_time = timings[query]
                best_index = index_type
        print(f"Fastest for {query}: {best_index} ({min_time:.6f} seconds)")
