import json
from flask import Flask, request, render_template, redirect, url_for, abort, redirect
from random import randint
from school_data import students, skills, courses
from api_functions import find_student, delete_student, create_student, get_student_data, add_student_skills, get_missing_skills

app = Flask(__name__, template_folder='./serving_static/templates', static_folder='./serving_static/static')


@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    student_data = get_student_data(id)
    if not student_data:
        abort(404)
    return render_template("student_display.html", student=student_data), 200

@app.route('/students', methods=['GET'])
def get_all_student():
    return json.dumps(students), 200

@app.route('/students', methods=['POST'])
def add_student():
    response_data = request.form.get
    student_created = create_student(response_data)
    if student_created:
        return redirect(url_for('students'), 201)
    else:
        return "student enrollment failed"

@app.route('/students/<id>/add_student_skills', methods=['GET'])
def add_student_skills_form(id):
    missing_skills = get_missing_skills(id)
    return render_template("add_student_skills.html", student=student, skills=missing_skills), 200

@app.route('/students/<id>/add_student_skills', methods=['POST'])
def add_student_skills(id):
    response_data = request.form.get
    add_student_skills(id, response_data)
    return redirect(url_for('students/' + id), 201)

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    student = find_student(id)
    delete_student(student)
    return "student deleted", 200


# Static file handlers

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/templates/new_student')
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