#!/usr/bin/python3

from psycopg.errors import ContainingSqlNotPermitted
import psycopg2 
from psycopg2 import sql, OperationalError, errors
from concurrent.futures import ThreadPoolExecutor, wait
import time
import argparse
import random
from Utils import dbname, user, password

import os



def transaction(transactionid, isolation_level, DB_PARAMS):
    while True:
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            conn.set_session(isolation_level=isolation_level)
            cur = conn.cursor()

            # Read employee balance
            cur.execute("SELECT balance FROM Accounts WHERE account = %s;", (transactionid,))
            e = cur.fetchone()[0]
            cur.execute("UPDATE Accounts SET balance = %s WHERE account = %s;", (e + 1, transactionid))

            cur.execute("SELECT balance FROM Accounts WHERE account = %s;", (0,))
            c = cur.fetchone()[0]
            cur.execute("UPDATE Accounts SET balance = %s WHERE account = %s;", (c - 1, 0))

            conn.commit()
            cur.close()
            conn.close()

            break  # success → break loop

        except (psycopg2.errors.SerializationFailure, psycopg2.errors.DeadlockDetected):
            # Retry on serialization failure or deadlock
            print(f"Transaction {transactionid} rolled back. Retrying...")
            conn.rollback()
            time.sleep(random.uniform(0.01, 0.1))  # small backoff

        except Exception as e:
            print(f"Transaction {transactionid} failed with error: {e}")
            if conn:
                conn.rollback()
            break  # exit loop on unexpected error

def get_balance(account_id, DB_PARAMS):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM Accounts WHERE account = %s;", (account_id,))
    balance = cur.fetchone()[0]
    cur.close()
    conn.close()
    return balance



def main():
    DB_PARAMS = {
    'dbname': dbname,
    'user': user,
    'password': password,
    'host': 'localhost',
    'port': 5432
    }

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--numthreads', type=int, default=1)
    parser.add_argument('-c', '--maxconcurrent', type=int, default=1)
    parser.add_argument('-i', '--isolation', choices=['read_committed', 'serializable'], default='read_committed')
    args = parser.parse_args()

    numthreads = args.numthreads
    maxconcurrent = args.maxconcurrent
    isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED if args.isolation == 'read_committed' else psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    c1 = get_balance(0, DB_PARAMS)

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=maxconcurrent) as executor:
        futures = {executor.submit(transaction, i + 1, isolation_level, DB_PARAMS): i for i in range(numthreads)}
        wait(futures)

    end_time = time.time()

# Measure c2
    c2 = get_balance(0, DB_PARAMS)

# Correctness metric
    correctness = (c1 - c2) / 100.0
    print(f"Correctness: {correctness}")

# Throughput
    duration = end_time - start_time
    print(f"Throughput (total time): {duration:.4f} seconds")
    print(f"Finished run with isolation={args.isolation}, concurrent workers={maxconcurrent}")
    print(f"Correctness: {correctness}")
    print(f"Throughput (total time): {duration:.4f} seconds")
    # Check if results.csv exists
    write_header = not os.path.exists("results.csv")

    with open("results.csv", "a") as f:
        if write_header:
            f.write("isolation,maxconcurrent,correctness,duration\n")
        f.write(f"{args.isolation},{maxconcurrent},{correctness},{duration:.4f}\n")




if __name__ == '__main__':
    main()
