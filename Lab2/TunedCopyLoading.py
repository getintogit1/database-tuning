#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbname, user, password 

'''    Using COPY instead of INSERT
    Every INSERT runs as a separate transaction (unless batched), which involves disk writes and logging.
    COPY bypasses this by writing data in large chunks, reducing overhead.   
    COPY writes data in binary or CSV mode, reducing I/O operations.
    INSERT executes multiple smaller disk writes, making it slower.
    Indexing impact (If the table has many indexes, inserting in batches may be beneficial).'''

tuplelimit = 1000
def optimize_db(cursor):
    print("Increasing work memory temporarily...")
    cursor.execute(f"GRANT pg_read_server_files TO {user}")                         
    cursor.execute("SET work_mem = '4GB';")                                     # Increase work_mem temporarily

def restore_db(cursor):
    print("Restoring database settings after data loading...")
    cursor.execute("RESET work_mem;")  # Reset work_mem to default

def copy_employee_data(file_path, cursor):
    with open(file_path, 'r') as file:
        next(file)  # Skip the header row
        cursor.copy_expert(
            "COPY employee (ssnum, name, manager, dept, salary, numfriends) FROM STDIN WITH CSV NULL ''",
            file
        )

def copy_student_data(file_path, cursor):                                          #cursor.copy_from() requires PostgreSQL superuser privileges.    with ope
    with open(file_path, 'r') as file:
        next(file)  # Skip header row
        cursor.copy_from(file, 'student', sep=',', columns=(
            'ssnum', 'name', 'course', 'grade'))

def copy_techDept_data(file_path, cursor):                                          #cursor.copy_from() requires PostgreSQL superuser privileges.    with ope
    with open(file_path, 'r') as file:
        next(file)  
        cursor.copy_expert(                                                         # copy expert fills the '' values to NULL so postgres dont complain about Integer != ""    
            "COPY techdept (dept, manager, location) FROM STDIN WITH CSV NULL ''",
            file
        )


def main():
    connection = psy.connect(
        host="localhost", 
        dbname=dbname, 
        user=user, 
        password=password, 
        port=5432
    )
    cursor = connection.cursor()
    print("Your data is loading this may take a while...")
    optimize_db(cursor)
    employeeData = "employees.csv"
    studentData = "students.csv"
    techDeptData = "techdepartments.csv"
    copy_employee_data(employeeData, cursor)
    copy_student_data(studentData, cursor)
    copy_techDept_data(techDeptData, cursor)
    restore_db(cursor)
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data loading complete for {employeeData} & {studentData} & {techDeptData}. ~CopyInsertScript.py")

if __name__ == "__main__":
    main()
