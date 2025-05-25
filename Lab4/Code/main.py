#!/usr/bin/env python3

import psycopg as psy
import time
from Setup.Utils import (
    dbname, user, password , 
    dropOldIndex, createClusteredBTree, 
    createNonClusteredBTree, 
    createHashIndex, explain_query)
from Setup.getUniqueParams import pubids, booktitles, years

def run_and_time(cursor, query, param_list, repetitions=1):
    start = time.time()
    for _ in range(repetitions):
        for params in param_list:
            cursor.execute(query, (params,))
            cursor.fetchall()
    end = time.time()
    total_queries = repetitions * len(param_list)
    return (end - start) / len(param_list)  # average time per query 


def pointQuery(cursor, repetitions=1):
    print("##### Point Query #####")
    query = "SELECT * FROM Publ WHERE pubID = %s;"
    explain_query(cursor, query, (pubids[10],))
    print("-" * 110)
    return run_and_time(cursor, query, [p.strip() for p in pubids], repetitions)


def multiPointQuery(cursor, repetitions=1):
    print("##### Multi Point #####")
    query = "SELECT * FROM Publ WHERE booktitle = %s;"
    explain_query(cursor, query, (booktitles[10],))
    print("-" * 110)
    return run_and_time(cursor, query, booktitles, repetitions)

def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def multiPointQueryInPredicate(cursor, repetitions=1, batch_size=10):
    print("##### Multipoint IN Predicate (Batched) #####")

    cleaned_pubids = [p.strip() for p in pubids]
    batches = list(chunked(cleaned_pubids, batch_size))
    
    # Explain query for the first batch only
    first_batch = batches[0]
    placeholders = ', '.join(['%s'] * len(first_batch))
    query = f"SELECT * FROM Publ WHERE pubID IN ({placeholders});"
    explain_query(cursor, query, tuple(first_batch))
    print("-" * 110)
    
    start = time.time()
    for _ in range(repetitions):
        for batch in batches:
            placeholders = ', '.join(['%s'] * len(batch))
            query = f"SELECT * FROM Publ WHERE pubID IN ({placeholders});"
            cursor.execute(query, tuple(batch))
            cursor.fetchall()
    end = time.time()
    
    total_queries = repetitions * len(batches)
    return (end - start) / total_queries  # average time per batch



def multiPointQueryHighSelectivity(cursor, repetitions=1):
    print("##### High Selective Multipoint #####")
    query = "SELECT * FROM Publ WHERE year = %s;"
    explain_query(cursor, query, (years[10],))
    print("-" * 110)
    return run_and_time(cursor, query, years, repetitions)


def run_experiment(create_index_func, repetitions=1):
    print(f"!!! ##### Running: {create_index_func.__name__} ##### !!!")
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
        "pointQuery":  pointQuery(cursor, repetitions),
        "Multipoint": multiPointQuery(cursor, repetitions),
        "Multipoint IN": multiPointQueryInPredicate(cursor, repetitions),
        "High selectivity": multiPointQueryHighSelectivity(cursor, repetitions)
    }
    
    cursor.close()
    connection.close()
    print(result)
    return result





if __name__ == "__main__":
    repetitions = 1  # Increase until total runtime > 60s
    result = {
        "Clustered BTree": run_experiment(createClusteredBTree, repetitions),
        "Non Clustered BTree": run_experiment(createNonClusteredBTree, repetitions),
        "Hash Index": run_experiment(createHashIndex, repetitions),
        "Table Scan": run_experiment(lambda cursor: None, repetitions)
    }

    query_types = ["pointQuery", "Multipoint", "Multipoint IN", "High selectivity"]
    for query in query_types:
        min_time = float("inf")
        best_index = None
        for index_type, timings in result.items():
            if timings[query] < min_time:
                min_time = timings[query]
                best_index = index_type
        print(f"Fastest for {query}: {best_index} ({min_time:.6f} seconds)")
