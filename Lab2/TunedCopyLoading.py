#!/usr/bin/env python3
import csv
import psycopg2 as psy
import Utils
from itertools import islice
from Utils import dbname, user, password, dbSetup

'''    Using COPY instead of INSERT
    Every INSERT runs as a separate transaction (unless batched), which involves disk writes and logging.
    COPY bypasses this by writing data in large chunks, reducing overhead.   
    COPY writes data in binary or CSV mode, reducing I/O operations.
    INSERT executes multiple smaller disk writes, making it slower.
    Indexing impact (If the table has many indexes, inserting in batches may be beneficial).'''

def clear_tables(cursor, connection):
    try:
        cursor.execute("DELETE FROM employee;")
        cursor.execute("DELETE FROM student;")
        cursor.execute("DELETE FROM techdept;")
        connection.commit()
        print("Tables cleared successfully.")
    except Exception as e:
        print(f"Error clearing tables: {e}")
        connection.rollback()


tuplelimit = 1000
def optimize_db(cursor):
    print("Increasing work memory temporarily...")
    cursor.execute(f"GRANT pg_read_server_files TO {user}")                         
    cursor.execute("SET work_mem = '4GB';")                                     # Increase work_mem temporarily

def restore_db(cursor):
    print("Restoring database settings after data loading...")
    cursor.execute("RESET work_mem;")  # Reset work_mem to default

def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = tuple(islice(it, n))
        if not batch:
            return
        yield batch

def copy_employee_data(file_path, cursor):
    with open(file_path, 'r') as file:
        if Utils.use_sqlite3:
            dr = csv.DictReader(file)
            for batch in batched(dr, 5000):
                to_db = [list(i.values()) for i in batch]
                cursor.executemany("INSERT INTO employee (ssnum, name, manager, dept, salary, numfriends) VALUES (?, ?, ?, ?, ?, ?)", to_db)
        else:
            next(file)  # Skip the header row
            cursor.copy_expert(
                "COPY employee (ssnum, name, manager, dept, salary, numfriends) FROM STDIN WITH CSV NULL ''",
                file
            )

def copy_student_data(file_path, cursor):                                          #cursor.copy_from() requires PostgreSQL superuser privileges.    with ope
    with open(file_path, 'r') as file:
        if Utils.use_sqlite3:
            dr = csv.DictReader(file)
            for batch in batched(dr, 5000):
                to_db = [list(i.values()) for i in batch]
                cursor.executemany("INSERT INTO student (ssnum, name, course, grade) VALUES (?, ?, ?, ?)", to_db)
        else:
            next(file)  # Skip header row
            cursor.copy_from(file, 'student', sep=',', columns=(
                'ssnum', 'name', 'course', 'grade'))

def copy_techDept_data(file_path, cursor):                                          #cursor.copy_from() requires PostgreSQL superuser privileges.    with ope
    with open(file_path, 'r') as file:
        if Utils.use_sqlite3:
            dr = csv.DictReader(file)
            for batch in batched(dr, 5000):
                to_db = [list(i.values()) for i in batch]
                cursor.executemany("INSERT INTO techdept (dept, manager, location) VALUES (?, ?, ?)", to_db)
        else:
            next(file)  
            cursor.copy_expert(                                                         # copy expert fills the '' values to NULL so postgres dont complain about Integer != ""    
                "COPY techdept (dept, manager, location) FROM STDIN WITH CSV NULL ''",
                file
            )


def main():
    connection = dbSetup(dbname, user, password)
    cursor = connection.cursor()
    print("Your data is loading this may take a while...")
    if not Utils.use_sqlite3:
        optimize_db(cursor)
    employeeData = "employees.csv"
    studentData = "students.csv"
    techDeptData = "techdepartments.csv"
    clear_tables(cursor, connection)
    copy_employee_data(employeeData, cursor)
    copy_student_data(studentData, cursor)
    copy_techDept_data(techDeptData, cursor)
    if not Utils.use_sqlite3:
        restore_db(cursor)
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data loading complete for {employeeData} & {studentData} & {techDeptData}. ~CopyInsertScript.py")

if __name__ == "__main__":
    main()
    Utils.use_sqlite3 = True
    main()
