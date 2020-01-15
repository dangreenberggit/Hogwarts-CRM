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

def add_skills(student, get, type):
    print("adding courses of type: " + type)
    if type == "possessed":
        student_data = student["data"]["student_skills"]
        skill_get = "skill"
        skill_type = "students_with_skill"
    if type == "desired":
        student_data = student["data"]["desired_skills"]
        skill_get = "desskill"
        skill_type = "students_desiring_skill"

    for skill in skills:
        skill_data = skill["data"][skill_type]
        skill_button = skill["id"] + skill_get
        skill_level = get(skill_button)
        if int(skill_level) > 0:
            new_skill = {
                "skill": skill["id"],
                "level": skill_level,
            }
            student_data.append(new_skill)
            skill_data.append(student["id"])
            print("course added")



def add_courses(student, get):
    print("adding courses")
    for course in courses:
        course_button = course["id"] + "course"
        course_check = get(course_button)
        if course_check == "on":
            student["data"]["desired_courses"].append(course["id"])
            course["data"]["students_interested"].append(student["id"])
            print("course added")


def student_template():
    new_student = {
        "id": "",
        "data": {
            "first_name": "",
            "last_name": "",
            "student_skills": [],
            "desired_skills": [],
            "desired_courses": [],
        },
    }
    return new_student


def create_student(get):

    student_id = generate_id(students)

    new_student = student_template()
    new_student["id"] = student_id
    new_student["data"]["first_name"], new_student["data"]["last_name"] = get('first_name'), get('last_name')

    if check_existing_student(new_student):
        return "Error: Student already exists!"

    add_skills(new_student, get, "possessed")
    add_skills(new_student, get, "desired")
    add_courses(new_student, get)
    students.append(new_student)

    return new_student
