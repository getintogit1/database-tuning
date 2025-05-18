#!/usr/bin/env python3
import time
import subprocess
import psycopg2
import Tuned
from Utils import dbname, password, user

print(user)
# Function to clear the tables 
def clear_tables():
    connection = psycopg2.connect(
        host="localhost", 
        dbname=dbname, 
        user=user, 
        password=password, 
        port=5432
    )
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM auth;")
        cursor.execute("DELETE FROM publ;")
        connection.commit()
        print("Tables cleared successfully.")
    except Exception as e:
        print(f"Error clearing tables: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Here we are actually Measuring everything 
def measure_execution_time(script_name):
    start_time = time.time()  
    try:        
        subprocess.run(['py', script_name], check=True)  
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_name}: {e}")
        return None
    end_time = time.time() 
    
    return end_time - start_time                                                # Return the time difference )

def main():
    clear_tables()
    #print("Running Naive.py")
    #naive_time = measure_execution_time('Naive.py')
    #print(f"Naive.py execution time: {naive_time:.4f} seconds")
    #clear_tables()
    print("Running Tuned.py")
    tuned_time = measure_execution_time('Tuned.py')
    print(f"Tuned.py execution time: {tuned_time:.4f} seconds")
    #clear_tables()
    #print("Running Tuned2.py")
    #tuned_time = measure_execution_time('Tuned2.py')
    #print(f"Tuned2.py execution time: {tuned_time:.4f} seconds")

if __name__ == "__main__":
    main()
