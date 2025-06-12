#!/usr/bin/python3

import psycopg2 
import time
from Utils import dbname, user, password, parse_arguments, write_csv
from concurrent.futures import ThreadPoolExecutor, wait
from solution_A_and_B import solutionA, solutionB, get_balance





def main():
    DB_PARAMS = {
    'dbname': dbname,
    'user': user,
    'password': password,
    'host': 'localhost',
    'port': 5432
    }


    args = parse_arguments()
    numthreads = args.numthreads
    maxconcurrent = args.maxconcurrent
    isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED if args.isolation == 'read_committed' else psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
    solution = args.solution

    if solution == "a":
        transaction = solutionA

    if solution == "b":
        transaction = solutionB

    c1 = get_balance(0, DB_PARAMS)
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=maxconcurrent) as executor:
        futures = {executor.submit(transaction, i + 1, isolation_level, DB_PARAMS): i for i in range(numthreads)}
        wait(futures)

    end_time = time.time()
    c2 = get_balance(0, DB_PARAMS)

    correctness = (c1 - c2) / 100.0
    print(f"Correctness: {correctness}")

    duration = end_time - start_time

    write_csv(args, maxconcurrent, correctness, duration)


if __name__ == '__main__':
    main()
