#!/usr/bin/env python3
import psycopg2 as psy
from Utils import dbSetup, dbname, user, password

connection = dbSetup(dbname, user, password)
def createTables(connection):
    try:
        cursor = connection.cursor() 
        cursor.execute("""
        CREATE TABLE Employee (
            ssnum SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            manager INTEGER,
            dept TEXT,
            salary NUMERIC(10,2),
            numfriends INTEGER
        );
        CREATE UNIQUE INDEX idx_employee_ssnum ON Employee(ssnum);
        CREATE UNIQUE INDEX idx_employee_name ON Employee(name);
        CREATE INDEX idx_employee_dept ON Employee(dept);

        CREATE TABLE Student (
            ssnum SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL,
            grade CHAR(2)
        );
        CREATE UNIQUE INDEX idx_student_ssnum ON Student(ssnum);
        CREATE UNIQUE INDEX idx_student_name ON Student(name);

        CREATE TABLE Techdept (
            dept TEXT PRIMARY KEY,
            manager INTEGER,
            location TEXT
        );
        CREATE UNIQUE INDEX idx_techdept_dept ON Techdept(dept);

        -- Foreign key constraints
        ALTER TABLE Employee ADD CONSTRAINT fk_employee_manager 
            FOREIGN KEY (manager) REFERENCES Employee(ssnum) ON DELETE SET NULL;
        
        ALTER TABLE Techdept ADD CONSTRAINT fk_techdept_manager 
            FOREIGN KEY (manager) REFERENCES Employee(ssnum) ON DELETE SET NULL;
        """)
        
        connection.commit()
        print("Tables Employee, Student, and Techdept created successfully.")
    
    except Exception as e:
        print("Error creating tables:", e)
    
    finally:
        cursor.close()
        connection.close()

createTables(connection)
