#!/usr/bin/env python3
import time
import subprocess
import psycopg2
from Utils import dbname, password, user

# Here we are actually Measuring everything 
def measure_execution_time(script_name):
    start_time = time.time()  
    try:        
        subprocess.run(['python3', script_name], check=True)  
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_name}: {e}")
        return None
    end_time = time.time() 
    
    return end_time - start_time                                                # Return the time difference )

def main():
    naiveQueryFile = "NaiveQuery.py"
    tunedQueryFile = "TunedQuery.py"
    print(f"Running: {naiveQueryFile}")
    naive_time = measure_execution_time(naiveQueryFile)
    print(f"Naive.py execution time: {naive_time:.4f} seconds")
    
    print(f"Running: {tunedQueryFile}")
    tuned_time = measure_execution_time(tunedQueryFile)
    print(f"Tuned.py execution time: {tuned_time:.4f} seconds")
    
if __name__ == "__main__":
    main()
