from random import randint
from school_data import students, skills, courses

def find_student(id):
    for student in students:
        if student["id"] == id:
            return student

def check_existing_student(new_student):
    for student in students:
        if student_name(new_student) == student_name(student):
            return True
    return False

def student_name(student):
    student_name = student["data"]["first_name"] + student["data"]["last_name"]
    return student_name

def generate_id(type):
    id = str(randint(0, 500))
    for item in type:
        while item["id"] == id:
            id = str(randint(0, 500))
    return id
