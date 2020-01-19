import json
from flask import Flask, request, render_template, redirect, url_for, abort, redirect
from random import randint
from school_data import students, skills, courses
from api_functions import find_student, delete_student, create_student, get_student_data, add_student_skills, add_courses, get_missing_skills, update_student_skills, get_student_list

app = Flask(__name__, template_folder='./serving_static/templates', static_folder='./serving_static/static')


@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    student_data = get_student_data(id)
    if not student_data:
        abort(404)
    return render_template("student_display.html", student=student_data), 200


@app.route('/students', methods=['GET'])
def get_all_student():
    student_list = get_student_list()
    return render_template("master_student_list.html", student_list=student_list), 200


@app.route('/students', methods=['POST'])
def add_student():
    response_data = request.form.get
    id = create_student(response_data)
    if not id:
        return "student enrollment failed"
    return redirect(url_for('get_student', id=id), 201)


@app.route('/students/<id>/add_skills', methods=['GET'])
def add_student_skills_form(id):
    student = find_student(id)
    missing_skills = get_missing_skills(id)
    return render_template("add_student_skills.html", student=student, skills=missing_skills), 200


@app.route('/students/<id>/add_skills', methods=['POST'])
def add_student_skills_route(id):
    response_data = request.form.get
    add_student_skills(id, response_data)
    return redirect(url_for('get_student', id=id), 201)


@app.route('/students/<id>/update_skills', methods=['GET'])
def update_student_skills_form(id):
    student_data = get_student_data(id)
    return render_template("update_student_skills.html", student=student_data), 200


@app.route('/students/<id>/update_skills', methods=['POST'])
def update_student_skills_route(id):
    response_data = request.form.get
    update_successful = update_student_skills(id, response_data)
    if update_successful:
        return redirect(url_for('get_student', id=id), 201)
    else:
        return "student update failed"


@app.route('/students/<id>/update_courses', methods=['GET'])
def update_student_courses_form(id):
    student_data = find_student(id)
    return render_template("update_courses.html", student=student_data, courses=courses), 200


@app.route('/students/<id>/update_courses', methods=['POST'])
def update_student_courses(id):
    response_data = request.form.get
    student = find_student(id)
    add_courses(student, response_data)
    return redirect(url_for('get_student', id=id), 201)


@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    student = find_student(id)
    delete_student(student)
    return "student deleted", 200


# Static file handlers

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/new_student')
def catalog_display():
    return render_template("new_student.html", skills=skills, courses=courses)


@app.route('/serving_static/static/<path:path>')
def static_root(path):
    return app.send_static_file(path)


@app.route('/serving_static/templates/<path:path>')
def temp_root(path):
    return render_template(path)


@app.route('/serving_static/static/css/<path:path>')
def stylesheets(path):
    return app.send_static_file('css/' + path)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)