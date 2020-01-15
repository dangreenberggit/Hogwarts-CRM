import json
from flask import Flask, request, render_template, redirect, url_for
from random import randint
from school_data import students, skills, courses
from api_functions import find_student, delete_student, create_student

app = Flask(__name__, template_folder='./serving_static/templates', static_folder='./serving_static/static')


@app.route('/student/<id>', methods=['GET'])
def get_student(id):
    student = find_student(id)
    return json.dumps(student)

@app.route('/student', methods=['GET'])
def get_all_student(id):
    return json.dumps(students)

@app.route('/add_student', methods=['POST'])
def add_student():
    response_data = request.form.get
    student_created = create_student(response_data)
    if student_created:
        return "student enrolled successfully"
    else:
        return "student enrollment failed"

@app.route('/student/<id>', methods=['DELETE'])
def delete_student(id):
    student = find_student(id)
    delete_student(student)
    return "student deleted"


# Static file handlers

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/templates/new_student.html')
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
    response = request.post("http://localhost:7000/add_student/")
