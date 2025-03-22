#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbname, user, password 


connection = psy.connect(
        host="localhost", 
        dbname=dbname, 
        user=user, 
        password=password, 
        port=5432
    )
cursor = connection.cursor()
print("Your data is loading this may take a while...")
# Tuned APPROACH 
''' The tuned approach is from the slides : Start-Up Costs Are High; Running Costs Are Low
    We try to parse and optimize the query only once and cache the execution plan. 
    The query can be executed repeatedly with different parameters without going through the parsing and optimization 
    steps again
    We also dont commit after every single line instead only one time for the both table loadings. 

    How Does It Work?
    When you issue a prepared statement, PostgreSQL:
    Step1: Compiles the SQL statement once.
           Caches the query’s execution plan.
    Step2: Executes the query multiple times with different values, without re-parsing or re-optimizing it.

    Batching:
    Collects Multiple Rows → Instead of inserting one row at a time, the script stores multiple rows in a batch (list).
    Executes in Bulk → When the batch reaches batch_size, all rows are inserted at once using executemany().
    Flush Remaining Data → After reading all lines, any leftover rows in the batch are inserted.
    Reduces SQL Overhead → Instead of sending 1000 queries, it sends 1 query with 1000 rows.
    Faster Execution → Fewer network round-trips & less parsing/optimization in PostgreSQL.
    Efficient Use of Transactions → Commits less frequently, reducing write lock contention.

    Bulk Upload Created Statement
    Pass a SQL query with placeholders (%s)
    Provide a list of tuples (each tuple = one row)
    Executes all rows in one go!
    Sends all data in one request → Reduces network overhead
    Uses fewer transactions → Improves database efficiency
    Less Python loop overhead → More performance
    Runs as a single SQL statement with a size of: {tuplelimit}
    '''

tupleLimit = 100000000

def insert_auth_data(file_path, batch_size=1000):
    # Prepare the insert query
    cursor.execute("""
        PREPARE insert_auth AS
        INSERT INTO Auth (name, pubID)
        VALUES ($1, $2);
    """)
    
    count = 0
    batch = []
    
    with open(file_path, 'r') as file:
        next(file)  # Skip header row
        for line in file:
            if count >= tupleLimit:
                break
            columns = line.strip().split('\t')  
            name = columns[0]
            pubID = columns[1]
            batch.append((name, pubID))
            # If batch size reached, execute the batch
            if len(batch) >= batch_size:
                execute_batch(batch)
                batch = []  # Reset batch after execution
            count += 1
    # Execute any remaining data in the batch
    if batch:
        execute_batch(batch)


def execute_batch(batch):
    # This function takes a batch of rows and inserts them all at once.
    insert_query = "EXECUTE insert_auth "
    # Create a list of placeholders for all rows in the batch
    placeholders = ', '.join(['(%s, %s)'] * len(batch))
    values = [item for sublist in batch for item in sublist]  # Flatten the batch list into a single list of values
    # Execute the batch insert
    cursor.execute(f"INSERT INTO Auth (name, pubID) VALUES {placeholders};", values)


def insert_publ_data(file_path, batch_size=1000):
    # Step 1: Prepare the SQL statement
    cursor.execute("""
        PREPARE insert_publ AS
        INSERT INTO Publ (pubID, type, title, booktitle, year, publisher)
        VALUES ($1, $2, $3, $4, $5, $6);
    """)

    count = 0
    batch = []
    
    with open(file_path, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            if count >= tupleLimit:
                break
            columns = line.strip().split('\t')
            if len(columns) < 5: # if a whole attribute is missing 
                columns += [""] * (6 - len(columns))  # Fill missing columns            
            while len(columns) < 6: #if publisher is unknown : replace "" with "unknown"
                columns.append("Unknown")            
            pubID, type_, title, booktitle, year, publisher = columns
            # Accumulate rows in the batch
            batch.append((pubID, type_, title, booktitle, year, publisher))
            # If batch size is reached, execute the batch
            if len(batch) >= batch_size:
                execute_batch_publ(batch)
                batch = []  # Reset batch after execution
            count += 1
    # If there are remaining rows in the batch, execute them
    if batch:
        execute_batch_publ(batch)


def execute_batch_publ(batch):
    # This function takes a batch of rows and inserts them all at once.
    insert_query = "EXECUTE insert_publ "
    # Create a list of placeholders for all rows in the batch
    placeholders = ', '.join(['(%s, %s, %s, %s, %s, %s)'] * len(batch))
    # Flatten the batch list into a single list of values
    values = [item for sublist in batch for item in sublist]
    # Execute the batch insert
    cursor.execute(f"INSERT INTO Publ (pubID, type, title, booktitle, year, publisher) VALUES {placeholders};", values)

filepath1 = 'auth.tsv'
filepath2 = 'publ.tsv'
insert_auth_data(filepath1)
insert_publ_data(filepath2) 
connection.commit()
cursor.close()
connection.close()
print(f"Data loading complete for {filepath1} & {filepath2}. ~Tuned.py")


