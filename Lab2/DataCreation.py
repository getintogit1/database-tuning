import csv
import random
import string
from faker import Faker


faker = Faker()                                                                 # random name generator 


TOTAL_EMPLOYEES = 100000
TOTAL_STUDENTS = 100000
OVERLAP = 6000                     # Number of people who are both employees and students
TOTAL_TECHDEPTS = 10

ssnum_counter = 1
generated_names = set()

def generate_unique_name():
    while True:
        name = faker.name()
        if name not in generated_names:
            generated_names.add(name)
            return name

def generate_people():
    global ssnum_counter
    people = []

    total_people = TOTAL_EMPLOYEES + TOTAL_STUDENTS - OVERLAP

    for _ in range(total_people):
        people.append({
            "ssnum": ssnum_counter,
            "name": generate_unique_name()
        })
        ssnum_counter += 1

    return people

def generate_employees(people, filename="employees.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ssnum", "name", "manager", "dept", "salary", "numfriends"])

        employee_pool = people[:TOTAL_EMPLOYEES]
        employees = []

        for person in employee_pool:
            manager = random.choice(employees) if employees else None
            dept = f"TechDept{random.randint(1, TOTAL_TECHDEPTS)}" if random.random() < 0.1 else None
            salary = round(random.uniform(30000, 150000), 2)
            numfriends = random.randint(0, 100)

            writer.writerow([
                person["ssnum"],
                person["name"],
                manager["ssnum"] if manager else None,
                dept,
                salary,
                numfriends
            ])

            employees.append(person)

    print(f"Generated {len(employee_pool)} employees in {filename}")

def generate_students(people, filename="students.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ssnum", "name", "course", "grade"])

        student_pool = people[-TOTAL_STUDENTS:]                                 # Ensures overlap
        for person in student_pool:
            course = random.choice(["Math", "Physics", "CS", "Biology", "History"])
            grade = random.choice(["A", "B", "C", "D", "F"])

            writer.writerow([
                person["ssnum"],
                person["name"],
                course,
                grade
            ])

    print(f"Generated {len(student_pool)} students in {filename}")

def generate_tech_departments(filename="techdepartments.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["dept", "manager", "location"])  

        for i in range(1, TOTAL_TECHDEPTS + 1):
            dept = f"TechDept{i}"
            manager = random.randint(1, TOTAL_EMPLOYEES)                        # Managers come from Employee table
            location = random.choice(["New York", "San Francisco", "Chicago", "Austin", "Seattle"])

            writer.writerow([dept, manager, location])

    print(f"Generated {TOTAL_TECHDEPTS} technical departments in {filename}")

def main():
    people_pool = generate_people()
    generate_employees(people_pool)
    generate_students(people_pool)    
    generate_tech_departments()

if __name__ == "__main__":
    main()

