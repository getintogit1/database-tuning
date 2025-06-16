#!/usr/bin/python3

import psycopg2
import random
import time


def solutionA(transactionid, isolation_level, DB_PARAMS):
    while True:
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            conn.set_session(isolation_level=isolation_level)
            cur = conn.cursor()

            cur.execute("SELECT balance FROM Accounts WHERE account = %s;", (transactionid,))
            e = cur.fetchone()[0]
            cur.execute("UPDATE Accounts SET balance = %s WHERE account = %s;", (e + 1, transactionid))
            
            cur.execute("SELECT balance FROM Accounts WHERE account = %s;", (0,))
            c = cur.fetchone()[0]
            cur.execute("UPDATE Accounts SET balance = %s WHERE account = %s;", (c - 1, 0))
            conn.commit()
            
            cur.close()
            conn.close()

            break  

        except (psycopg2.errors.SerializationFailure, psycopg2.errors.DeadlockDetected):
            print(f"Transaction {transactionid} rolled back. Retrying...")
            conn.rollback()
            time.sleep(random.uniform(0.01, 0.1))  

        except Exception as e:
            print(f"Transaction {transactionid} failed with error: {e}")
            if conn:
                conn.rollback()
            break  

def get_balance(account_id, DB_PARAMS):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM Accounts WHERE account = %s;", (account_id,))
    balance = cur.fetchone()[0]
    cur.close()
    conn.close()
    return balance

def solutionB(transactionid, isolation_level, DB_PARAMS):
    while True:
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            conn.set_session(isolation_level=isolation_level)
            cur = conn.cursor()
            cur.execute("UPDATE Accounts SET balance = balance + 1 WHERE account = %s;", (transactionid,))
            cur.execute("UPDATE Accounts SET balance = balance -1 WHERE account = 0;")
            cur.close()
            conn.commit()
            conn.close()
            break  

        except (psycopg2.errors.SerializationFailure, psycopg2.errors.DeadlockDetected):
            print(f"Transaction {transactionid} rolled back. Retrying...")
            conn.rollback()
            time.sleep(random.uniform(0.01, 0.1))  

        except Exception as e:
            print(f"Transaction {transactionid} failed with error: {e}")
            if conn:
                conn.rollback()
            break  


