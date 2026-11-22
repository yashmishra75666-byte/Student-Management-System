import sqlite3

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students
(
    roll TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    branch TEXT,
    semester INTEGER
)
""")

conn.commit()

print("====================================================================================================")
print("                             STUDENT MANAGEMENT SYSTEM                                              ")
print("====================================================================================================")

while True:

    print("1. Add Student")
    print("2. View Student")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Add Total Students")
    print("7. View Student by Branch")
    print("8. View Student by Semester")
    print("9. Sort Student by Name")
    print("10. Add Student by Age")
    print("11. Exit")

    choice = input("\nEnter your choice (1-7): ")
    if choice == "1":
        print("\nAdd New Student")

        roll = input("Enter Roll Number: ")
        name = input("Enter Name: ").strip()
        branch = input("Enter Branch: ").strip()

        if not name or not branch:
            print("Name and Branch cannot be empty!")
            continue

        try:
            age = int(input("Enter Age: "))
            semester = int(input("Enter Semester: "))
            if age <= 0:
               print("Age must be greater than 0!")
               continue

            if semester < 1 or semester > 8:
               print("Semester must be between 1 and 8!")
               continue
        except ValueError:
            print("Please enter numbers only!")
            continue
        try:
            cursor.execute("""
            INSERT INTO students (roll, name, age, branch, semester)
            VALUES (?, ?, ?, ?, ?)
            """, (roll, name, age, branch, semester))

            conn.commit()
            print("Student Added Successfully!")

        except sqlite3.IntegrityError:
            print("Error: Roll Number already exists!")
    elif choice == '2':
        print("\nAll Students")

        cursor.execute("SELECT * FROM students")

        records = cursor.fetchall()

        if records:
            for student in records:
                print("--------------------")
                print("Roll Number:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Branch:", student[3])
                print("Semester:", student[4])

        else:
            print("No students found!")
    elif choice == '3':
        print("1. Search by Roll Number")
        print("2. Search by Name")

        search_choice = input("Choose search option: ")
        roll = input("Enter Roll Number: ")
        
        if search_choice == "1":
           roll = input("Enter Roll Number: ")
           cursor.execute(
               "SELECT * FROM students WHERE roll = ?", (roll,)
    )
           students = cursor.fetchall()

        elif search_choice == "2":
            name = input("Enter Student Name: ")
            cursor.execute(
                "SELECT * FROM students WHERE name LIKE ?", 
                ('%' + name + '%',)
            )
            students = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM students WHERE roll = ?", (roll,)
        )
        student = cursor.fetchone()

        if student:
            print("\n==========================")
            print("      STUDENT PROFILE")
            print("==========================")
            print("Roll Number :", student[0])
            print("Name        :", student[1])
            print("Age         :", student[2])
            print("Branch      :", student[3])
            print("Semester    :", student[4])
            print("==========================")

        else:
            print("Student Not Found!")
    elif choice == '4':

        roll = input("Enter Roll Number to Update: ")

        cursor.execute(
            "SELECT * FROM students WHERE roll = ?",
            (roll,)
        )

        student = cursor.fetchone()

        if student:
            print("\nStudent Found!")
            print("Current Name:", student[1])
            print("Current Age:", student[2])
            print("Current Branch:", student[3])
            print("Current Semester:", student[4])

            name = input("Enter New Name: ").strip()
            branch = input("Enter New Branch: ").strip()

            if not name or not branch:
                print("Name and Branch cannot be emprty!")
                continue

            try:
                age = int(input("Enter New Age: "))
                semester = int(input("Enter New Semester: "))

            except ValueError:
                print("Please enter numbers only!")
                continue
            if age <= 0:
               print("Age must be greater than 0!")
               continue

            if semester < 1 or semester > 8:
                print("Semester must be between 1 and 8!")
                continue

            cursor.execute("""
                UPDATE students
                SET name = ?, age = ?, branch = ?, semester = ?
                WHERE roll = ?
                """, (name, age, branch, semester, roll))

            conn.commit()

            print("Student Updated Successfully!")

        else:
            print("Student Not Found!")

    elif choice == '5':
        
        roll = input("Enter Roll Number to Delete: ")
        if not roll.strip():
            print("Roll Number cannot be empty!")
            continue
        cursor.execute("SELECT * FROM students WHERE roll = ?", (roll,))
        student = cursor.fetchone()

        if student:
            print("Student Found!")
            
            print("\nStudent Details:")
            print("Roll Number:", student[0])
            print("Name:", student[1])
            print("Branch:", student[3])
            print("Semester:", student[4])
            
            confirm = input("Are you sure you want to delete? (yes/no): ")

            if confirm.lower() == "yes":
                cursor.execute("DELETE FROM students WHERE roll = ?", (roll,))
                conn.commit()
                print("Student Deleted Successfully!")
            else:
                print("Delete Cancelled!")
        else:
            print("Student Not Found!")

    
    elif choice == "6":
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()

        print("Total Students:", total[0])
    
    elif choice == "7":

        branch = input("Enter Branch Name: ")

        cursor.execute(
        "SELECT * FROM students WHERE LOWER(branch) = LOWER(?)",
        (branch,)
    )

    students = cursor.fetchall()

    if students:
        print("\nStudents in", branch, "Branch")

        for student in students:
            print("----------------------")
            print("Roll Number:", student[0])
            print("Name:", student[1])
            print("Age:", student[2])
            print("Branch:", student[3])
            print("Semester:", student[4])

        else:
            print("No Students Found in this Branch!")
   
    elif choice == "8":

        semester = int(input("Enter Semester: "))

        cursor.execute(
        "SELECT * FROM students WHERE semester = ?",
        (semester,)
    )

        students = cursor.fetchall()

        if students:
            print("\nStudents in Semester", semester)

            for student in students:
                print("----------------------")
                print("Roll Number:", student[0])
                print("Name:", student[1])
                print("Branch:", student[3])
                print("Semester:", student[4])

        else:
            print("No Students Found!")
    
    elif choice == "9":

            cursor.execute(
                "SELECT * FROM students ORDER BY name ASC"
            )

            students = cursor.fetchall()

            if students:
                print("\nStudents Sorted by Name (A to Z)")

                for student in students:
                    print("----------------------")
                    print("Roll Number:", student[0])
                    print("Name:", student[1])
                    print("Age:", student[2])
                    print("Branch:", student[3])
                    print("Semester:", student[4])

            else:
                print("No Students Found!")
    
    elif choice == "10":

        cursor.execute(
            "SELECT * FROM students ORDER BY age ASC"
        )

        students = cursor.fetchall()

        if students:
            print("\nStudents Sorted by Age")

            for student in students:
                print("----------------------")
                print("Roll Number:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Branch:", student[3])
                print("Semester:", student[4])

        else:
            print("No Students Found!")
    
    elif choice == "11":
       print("Program Closed!")
       conn.close()
       break
    else:
        print("Invalide Choice")    

    print("Student Management System")

roll = input("Enter Roll Number: ")
name = input("Enter Student Name: ")
age = input("Enter Student Age: ")
branch = input("Enter Student branch: ")
semester = input("Enter Semester: ")

cursor.execute("""
INSERT INTO students (roll, name, age, branch, semester)
VALUES (?, ?, ?, ?, ?)
""", (roll, name, age, branch, semester))

conn.commit()

print("Student saved successfully!")

print("\nStudent Details")
print("Roll number: ",roll)
print("Name: ",name)
print("Age: ",age)
print("Branch: ",branch)
print("Semester: ",semester)

print("\nAll Students")

cursor.execute("SELECT * FROM students")

records = cursor.fetchall()

for student in records:
    print(student)

