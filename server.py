import json
from flask import Flask, request, render_template, redirect, url_for
from random import randint
from school_data import students, skills, courses
from api_functions import find_student, check_existing_student, generate_id, create_student

app = Flask(__name__, template_folder='./serving_static/templates', static_folder='./serving_static/static')


@app.route('/get_student/<id>', methods=['GET'])
def get_student(id):
    student = find_student(id)
    return json.dumps(student)

@app.route('/add_student', methods=['POST'])
def add_student():
    new_student = create_student(request.form.get)
    print("new_student post process complete")
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
