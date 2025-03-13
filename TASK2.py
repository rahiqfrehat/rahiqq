class Student:
    def __init__(self, name, age, mark):
        self.name = name
        self.age = age
        self.mark = mark

    def __str__(self):
        return f"{self.name} (Age: {self.age}, Mark: {self.mark})"
    students = [
    Student("Ali", 20, 85),
    Student("Sara", 19, 45),
    Student("Khalid", 21, 60),
    Student("Noor", 22, 30),
    Student("Omar", 18, 75)
]

success_students = [student for student in students if student.mark >= 50]
failed_students = [student for student in students if student.mark < 50]
print("Success Students:")
for student in success_students:
    print(f"- {student}")

print("\nFailed Students:")
for student in failed_students:
    print(f"- {student}")