import csv
import random
import string
from faker import Faker


faker = Faker()                                                                 # random name generator 


TOTAL_EMPLOYEES = 100000
TOTAL_STUDENTS = 100000
TOTAL_TECHDEPTS = 10  

ssnum_counter = 1

generated_names = set()
def generate_unique_name():
    while True:
        name = faker.name()
        if name not in generated_names:
            generated_names.add(name)
            return name


def generate_employees(filename="employees.csv"):
    global ssnum_counter
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ssnum", "name", "manager", "dept", "salary", "numfriends"])                                   # Header

        employees = []
        for _ in range(TOTAL_EMPLOYEES):
            ssnum = ssnum_counter
            name = generate_unique_name()
            manager = random.choice(employees) if employees else None
            dept = f"TechDept{random.randint(1, TOTAL_TECHDEPTS)}" if random.random() < 0.1 else None                   # 10% in tech dept
            salary = round(random.uniform(30000, 150000), 2)
            numfriends = random.randint(0, 100)

            writer.writerow([ssnum, name, manager.ssnum if manager else None, dept, salary, numfriends])
            employees.append(type("Emp", (), {"ssnum": ssnum, "name": name}))                                                         # Store ssnum reference
            ssnum_counter += 1

    print(f"Generated {TOTAL_EMPLOYEES} employees in {filename}")


def generate_students(filename="students.csv"):
    global ssnum_counter
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ssnum", "name", "course", "grade"])               #

        for _ in range(TOTAL_STUDENTS):
            ssnum = ssnum_counter
            name = generate_unique_name()
            course = random.choice(["Math", "Physics", "CS", "Biology", "History"])
            grade = random.choice(["A", "B", "C", "D", "F"])

            writer.writerow([ssnum, name, course, grade])
            ssnum_counter += 1

    print(f"Generated {TOTAL_STUDENTS} students in {filename}")

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
    generate_employees()
    generate_students()
    generate_tech_departments()

if __name__ == "__main__":
    main()

