import json
from flask import Flask, request, render_template, redirect, url_for
from random import randint
from school_data import students, skills, courses
from api_functions import find_student, check_existing_student, generate_id

app = Flask(__name__, template_folder='./serving_static/templates', static_folder='./serving_static/static')


@app.route('/get_student/<id>', methods=['GET'])
def get_student(id):
    student = find_student(id)
    return json.dumps(student)

@app.route('/add_student', methods=['POST'])
def add_student():
    student_id = generate_id(students)
    new_student = {
        "id": student_id,
        "data": {
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "student_skills": [],
            "desired_skills": [],
            "desired_courses": [],
        },
    }

    if check_existing_student(new_student):
        return "Error: Student already exists!"

    for skill in skills:
        possessed_skill_button = skill["id"] + "skill"
        desired_skill_button = skill["id"] + "desskill"
        possessed_skill = request.form.get(possessed_skill_button)
        desired_skill = request.form.get(desired_skill_button)
        if int(possessed_skill) > 0:
            new_skill = {
                "skill": skill["id"],
                "level": possessed_skill,
            }
            new_student["data"]["student_skills"].append(new_skill)
            skill["data"]["students_with_skill"].append(new_student["id"])
        if int(desired_skill) > 0:
            new_skill = {
                "skill": skill["id"],
                "level": desired_skill,
            }
            new_student["data"]["desired_skills"].append(new_skill)
            skill["data"]["students_desiring_skill"].append(new_student["id"])

    for course in courses:
        course_button = course["id"] + "course"
        course_check = request.form.get(course_button)
        if course_check == "on":
            new_student["data"]["desired_courses"].append(course["id"])
            course["data"]["students_interested"].append(new_student["id"])

    else:
        students.append(new_student)
    return json.dumps(new_student)

# Static file handlers

@app.route("/")
def homepage():
    return "Hogwarts CRM"


@app.route('/templates/new_student.html')
def catalog_display():
    return render_template("new_student.html", skills=skills, courses=courses)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
    response = request.post("http://localhost:7000/add_student/")
