from datetime import datetime
import random
import string
import psycopg2
import json

from flask import Flask, request, redirect

from form import create_form

app = Flask(__name__)

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    host="postgres_container",
    password="postgres",
    port="5432",
)


@app.route("/whoami")
def whoami():
    client_browser = request.user_agent.string
    client_ip = request.remote_addr
    current_time = datetime.now()

    return {
        "browser": client_browser,
        "ip": client_ip,
        "server_time": current_time,
    }


@app.route("/source_code")
def source_code():
    with open(__file__, "r") as f:
        code = f.read()

    return f"<pre>{code}</pre>"


@app.route("/random")
def random_string():
    try:
        length = int(request.args.get("length", 8))
        specials = int(request.args.get("special", 0))
        digits = int(request.args.get("digits", 0))

        if length < 1 or length > 100:
            return {
                "error": "Length must be between 1 and 100",
            }, 400
        if specials not in (0, 1) or digits not in (0, 1):
            return {"error": "Specials and Digits must be 0 or 1"}, 400

        characters = string.ascii_letters
        if digits:
            characters += string.digits
        if specials:
            characters += '!"№;%:?*()_+'

        result = "".join(random.choices(characters, k=length))

        return {"random_string": result}

    except ValueError:
        return {"error": "Invalid input"}, 400


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        body = request.form
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s);",
                (
                    body["email"],
                    body["password"],
                    body["first_name"],
                    body["last_name"],
                ),
            )
            conn.commit()
        return redirect("/users", code=302)

    return create_form("email", "password", "first_name", "last_name")


@app.route("/users")
def get_users():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        return json.dumps(cur.fetchall())


@app.route("/courses")
def get_courses():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM course;")
        return json.dumps(cur.fetchall())


@app.route("/courses/create", methods=["POST", "GET"])
def create_course():
    if request.method == "POST":
        body = request.form
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO course (name, teacher_id) VALUES (%s, %s) RETURNING id;",
                (
                    body["name"],
                    body["teacher_id"],
                ),
            )
            course_id = cur.fetchone()[0]

            student_ids = body.getlist("student_ids")
            for student_id in student_ids:
                cur.execute(
                    "INSERT INTO course_students (course_id, student_id) VALUES (%s, %s);",
                    (course_id, student_id),
                )
            conn.commit()
        return redirect("/courses", code=302)

    return create_form("name", "teacher_id", "student_ids")


@app.route("/courses/<course_id>")
def get_course(course_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT course.*, 
                   json_agg(DISTINCT student) AS students, 
                   json_agg(DISTINCT lesson) AS lessons, 
                   json_agg(DISTINCT task) AS tasks 
            FROM course 
            LEFT JOIN course_students ON course.id = course_students.course_id 
            LEFT JOIN users AS student ON course_students.student_id = student.id 
            LEFT JOIN lesson ON lesson.course_id = course.id 
            LEFT JOIN task ON task.course_id = course.id 
            WHERE course.id = %s 
            GROUP BY course.id;
            """,
            (course_id,),
        )
        return json.dumps(cur.fetchone())


@app.route("/courses/<course_id>/lectures", methods=["POST", "GET"])
def add_lectures(course_id):
    if request.method == "POST":
        body = request.form
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO lesson (course_id, name, description) VALUES (%s, %s, %s);",
                (course_id, body["name"], body["description"]),
            )
            conn.commit()
        return redirect(f"/courses/{course_id}", code=302)

    return create_form("name", "description")


@app.route("/courses/<course_id>/tasks", methods=["POST", "GET"])
def create_task(course_id):
    if request.method == "POST":
        body = request.form
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO task (course_id, description) VALUES (%s, %s);",
                (course_id, body["description"]),
            )
            conn.commit()
        return redirect(f"/courses/{course_id}", code=302)

    return create_form("description")


@app.route("/courses/<course_id>/tasks/<task_id>/answers", methods=["POST", "GET"])
def submit_answer(course_id, task_id):
    if request.method == "POST":
        body = request.form
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO answer (task_id, student_id, description) VALUES (%s, %s, %s);",
                (task_id, body["student_id"], body["description"]),
            )
            conn.commit()
        return redirect(f"/courses/{course_id}/tasks/{task_id}/answers", code=302)

    return create_form("description", "student_id")


@app.route(
    "/courses/<course_id>/tasks/<task_id>/answers/<answer_id>/mark",
    methods=["POST", "GET"],
)
def mark_answer(course_id, task_id, answer_id):
    if request.method == "POST":
        body = request.form
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO mark (answer_id, teacher_id, date, grade) VALUES (%s, %s, %s, %s);",
                (answer_id, body["teacher_id"], datetime.now(), body["grade"]),
            )
            conn.commit()
        return redirect(f"/courses/{course_id}", code=302)

    return create_form("teacher_id", "grade")


@app.route("/courses/<course_id>/rating", methods=["POST", "GET"])
def course_rating(course_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT student.id, student.first_name, student.last_name, AVG(mark.grade) AS avg_grade 
            FROM users AS student 
            JOIN course_students ON course_students.student_id = student.id 
            JOIN answer ON answer.student_id = student.id 
            JOIN mark ON mark.answer_id = answer.id 
            WHERE course_students.course_id = %s 
            GROUP BY student.id 
            ORDER BY avg_grade DESC;
            """,
            (course_id,),
        )
        return json.dumps(cur.fetchall())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
