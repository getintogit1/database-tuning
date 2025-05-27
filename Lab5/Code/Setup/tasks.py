#!/usr/bin/env python3
from Setup.Utils import dropOldIndex, createClusteredBTree,createNonClusteredBTree
import time 


def task1(cursor, querys):
    print("### TASK 1 IS STARTING ###")
    for query in querys:
        run_experiment(cursor,[None], query)
        run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID")], query)
        #i ve commented this line out because it has high run time, for final run we can uncomment  
        #run_experiment(cursor, [createClusteredBTree("Publ", "pubID"), createClusteredBTree("Auth", "pubID")], query)


def task2(cursor, querys): 
    print("### TASK 2 IS STARTING ###")
    cursor.execute("SET enable_hashjoin = false; ")
    cursor.execute("SET enable_mergejoin = false;")
    cursor.execute("SET enable_nestloop TO true;")
    cursor.execute("SHOW enable_nestloop;")
    result = cursor.fetchone()
    if result:
        print("enable_nestloop:", result[0])
    else:
       raise 
    for query in querys:
        run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID")], query)
        run_experiment(cursor, [createNonClusteredBTree("Auth", "pubID")], query)
        run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID"), createNonClusteredBTree("Auth", "pubID")], query)


def task3(cursor, querys):
    print("### TASK 3 IS STARTING ###")
    cursor.execute("SET enable_nestloop TO false;")
    cursor.execute("SET enable_hashjoin TO false;")
    cursor.execute("SET enable_mergejoin TO true;")
    cursor.execute("SHOW enable_mergejoin;")
    result = cursor.fetchone()
    if result:
        print("enable_mergejoin:", result[0])
    else:
        raise
    for query in querys:
        run_experiment(cursor, [None], query)
        run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID"), createNonClusteredBTree("Auth", "pubID")], query)
        run_experiment(cursor, [createClusteredBTree("Publ", "pubID"), createClusteredBTree("Auth", "pubID")], query)
  

def task4(cursor, querys):
    print("### TASK 4 IS STARTING ###")
    cursor.execute("SET enable_mergejoin TO false;")
    cursor.execute("SET enable_nestloop TO false;")
    cursor.execute("SET enable_hashjoin TO true;")
    cursor.execute("SHOW enable_hashjoin;")
    result = cursor.fetchone()
    if result:
        print("enable_hashjoin:", result[0])
    else:
        raise
    for query in querys:
        run_experiment(cursor, [None], query)
           

def run_query_with_timing(cursor, query):
 
    start = time.time()
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    output = cursor.fetchall()
    duration = time.time() - start
    return duration, "\n".join([line[0] for line in output])


def run_experiment(cursor, index_creators, query):
    dropOldIndex(cursor)
    if index_creators is None or index_creators == [None]:
        name = "No Index"
        index_creators = []  
    else:
        name = ", ".join(f"{fn.__name__}" for fn in index_creators)
    print(f"\n=== Running experiment: {name} ===")
    for creator in index_creators:
        creator(cursor)

    duration, plan = run_query_with_timing(cursor, query)
    print(plan)
    print(f"Execution time for '{name}': {duration:.4f} seconds\n")
    return {"name": name, "plan": plan, "time": duration}




