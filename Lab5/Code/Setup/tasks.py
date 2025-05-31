#!/usr/bin/env python3
from Setup.Utils import dropOldIndex, createClusteredBTree,createNonClusteredBTree
import time 


def task1(cursor, querys):
    print("### TASK 1 IS STARTING ###")
    result = []
    for i, query in enumerate(querys):
        result.append(run_experiment(cursor, [None], query, "Default (Planner's Choice)", i + 1))
        result.append(run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID")], query, "Default (Planner's Choice)", i + 1))
        result.append(run_experiment(cursor, [createClusteredBTree("Publ", "pubID"), createClusteredBTree("Auth", "pubID")], query, "Default (Planner's Choice)", i + 1))
    return result


def task2(cursor, querys): 
    print("### TASK 2 IS STARTING ###")
    cursor.execute("SET enable_hashjoin = false; ")
    cursor.execute("SET enable_mergejoin = false;")
    cursor.execute("SET enable_nestloop TO true;")
    cursor.execute("SHOW enable_nestloop;")
    response = cursor.fetchone()
    if response:
        print("enable_nestloop:", response[0])
    else:
       raise 
    result = []
    for i, query in enumerate(querys):
        result.append(run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID")], query,"Nested Loop", i + 1 ))
        result.append(run_experiment(cursor, [createNonClusteredBTree("Auth", "pubID")], query,"Nested Loop", i + 1))
        result.append(run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID"), createNonClusteredBTree("Auth", "pubID")], query,"Nested Loop", i + 1))
    return result


def task3(cursor, querys):
    print("### TASK 3 IS STARTING ###")
    cursor.execute("SET enable_nestloop TO false;")
    cursor.execute("SET enable_hashjoin TO false;")
    cursor.execute("SET enable_mergejoin TO true;")
    cursor.execute("SHOW enable_mergejoin;")
    response = cursor.fetchone()
    result = []
    if response:
        print("enable_mergejoin:", response[0])
    else:
        raise
    for i, query in enumerate(querys):
        result.append(run_experiment(cursor, [None], query,"Merge Join", i + 1))
        result.append(run_experiment(cursor, [createNonClusteredBTree("Publ", "pubID"), createNonClusteredBTree("Auth", "pubID")], query,"Merge Join", i + 1))
        result.append(run_experiment(cursor, [createClusteredBTree("Publ", "pubID"), createClusteredBTree("Auth", "pubID")], query,"Merge Join", i + 1))
    return result   

def task4(cursor, querys):
    print("### TASK 4 IS STARTING ###")
    cursor.execute("SET enable_mergejoin TO false;")
    cursor.execute("SET enable_nestloop TO false;")
    cursor.execute("SET enable_hashjoin TO true;")
    cursor.execute("SHOW enable_hashjoin;")
    response = cursor.fetchone()
    result = []
    if response:
        print("enable_hashjoin:", response[0])
    else:
        raise
    for i, query in enumerate(querys):
        result.append(run_experiment(cursor, [None], query, "Hash Join" ,i + 1))

    return result
           

def run_query_with_timing(cursor, query):
 
    start = time.time()
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    output = cursor.fetchall()
    duration = time.time() - start
    return duration, "\n".join([line[0] for line in output])


def run_experiment(cursor, index_creators, query,strategy_name, query_id):
    dropOldIndex(cursor)
    cursor.execute("""
    SELECT indexname
    FROM pg_indexes
    WHERE tablename IN ('publ', 'auth');    
    """)
    print("Indexes after drop:", [row[0] for row in cursor.fetchall()])
    
    if index_creators is None or index_creators == [None]:
        name = "No Index"
        index_creators = []
    else:
        name = ", ".join(f"{fn.__name__}" for fn in index_creators)
    print(f"\n=== Running experiment: {strategy_name} | {name} ===")
    
    for creator in index_creators:
        creator(cursor)

    duration, plan = run_query_with_timing(cursor, query)
    print(plan)
    print(f"Execution time for '{strategy_name} | {name}': {duration:.4f} seconds\n")
    
    return {
        "query_id": query_id,
        "strategy": strategy_name,
        "index": name,
        "time": duration
    }




