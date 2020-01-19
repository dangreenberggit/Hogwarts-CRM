from random import randint
from school_data import students, skills, courses

def find_student(id):
    for student in students:
        if student["id"] == id:
            return student
    return False


def delete_student(id):
    for student in students:
        if student["id"] == id:
            del student


def check_existing_student(new_student):
    for student in students:
        if get_student_name(new_student) == get_student_name(student):
            return True
    return False


def get_student_name(student):
    student_name = student["data"]["first_name"] + " " + student["data"]["last_name"]
    return student_name


def generate_id(type):
    id = str(randint(0, 500))
    id_list = []
    for item in type:
        id_list.append(item["id"])

    while id in id_list:
        id = str(randint(0, 500))

    return id


def new_skills(student, get, type):
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


def update_skills_by_type(student, get, kind):
    if kind == "possessed":
        student_data = student["data"]["student_skills"]
        skill_get = "skill"

    if kind == "desired":
        student_data = student["data"]["desired_skills"]
        skill_get = "desskill"

    for skill in student_data:
        skill_button = skill["skill"] + skill_get
        skill_level = get(skill_button)
        if skill_level and int(skill_level) > 0:
            skill["level"] = skill_level

        # skill_data.append(student["id"]) function to update student info under skills if skill dictionary not removed


def add_courses(student, get):
    for course in courses:
        course_button = course["id"] + "course"
        course_check = get(course_button)
        if course_check == "on":
            student["data"]["desired_courses"].append(course["id"])
            course["data"]["students_interested"].append(student["id"])


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

    #timestamp = datetime.datetime.now().str

    new_student = student_template()
    new_student["id"] = student_id
    new_student["data"]["first_name"], new_student["data"]["last_name"] = get('first_name'), get('last_name')

    if check_existing_student(new_student):
        return False

    new_skills(new_student, get, "possessed")
    new_skills(new_student, get, "desired")
    add_courses(new_student, get)
    students.append(new_student)

    return new_student["id"]


def list_skills(student):
    skill_list = []
    for skill in student["data"]["student_skills"]:
        skill_list.append(skill["skill"])
    return skill_list


def get_missing_skills(id):
    student = find_student(id)
    skill_list = list_skills(student)
    missing_skills = []

    for skill in skills:
        if not skill["id"] in skill_list:
            missing_skill = {
                "id": skill["id"],
                "name": skill["data"]["skill_name"],
            }
            missing_skills.append(missing_skill)

    return missing_skills


def add_student_skills(id, get):
    student = find_student(id)

    for skill in skills:
        skill_button = skill["id"] + "skill"
        skill_check = get(skill_button)
        if skill_check == "on":
            new_skill = {
                "skill": skill["id"],
                "level": "1",
            }
            student["data"]["student_skills"].append(new_skill)
            skill["data"]["students_with_skill"].append(student["id"])


def update_student_skills(id, get):
    student = find_student(id)

    if not check_existing_student(student):
        return False

    update_skills_by_type(student, get, "possessed")
    update_skills_by_type(student, get, "desired")

    return True


def get_list_from_data(student, student_data, data_type):
    student_data_list = []

    for student_item in student["data"][student_data]:
        student_data_object = {}
        for type_item in data_type:
            if (student_data == "desired_courses") and (student_item != type_item["id"]):
                continue
            elif (student_data == "desired_courses") and (student_item == type_item["id"]):
                student_data_object["name"] = type_item["data"]["course_name"]
                student_data_object["id"] = student_item
                student_data_list.append(student_data_object)
            elif (student_data == "student_skills" or "desired_skills") and (student_item["skill"] == type_item["id"]):
                student_data_object["name"] = type_item["data"]["skill_name"]
                student_data_object["level"] = student_item["level"]
                student_data_object["id"] = student_item["skill"]
                student_data_list.append(student_data_object)
    return student_data_list


def get_student_data(id):

    student = find_student(id)

    if not student:
        return False

    student_display_data = {
        "id": id,
        "name": student["data"]["first_name"] + " " + student["data"]["last_name"],
        "possessed_skills": get_list_from_data(student, "student_skills", skills),
        "desired_skills": get_list_from_data(student, "desired_skills", skills),
        "courses": get_list_from_data(student, "desired_courses", courses),
    }

    return student_display_data

def get_student_list():
    student_list = []
    for student in students:
        student_display_data = {
            "id_URL": '/students/' + student['id'],
            "name": student["data"]["first_name"] + " " + student["data"]["last_name"],
        }
        student_list.append(student_display_data)

    return student_list
