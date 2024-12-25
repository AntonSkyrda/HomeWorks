from datetime import datetime
import random
import string

from flask import Flask, request, redirect, jsonify
from sqlalchemy import select

from form import create_form
from models import Course, Lesson, User, Homework, HomeworkResponse, HomeworkGrade
from database import session


app = Flask(__name__)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        user = User(
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
        )
        session.add(user)
        session.commit()
        return (
            jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                },
            ),
            201,
        )
    return create_form("email", "password", "first_name", "last_name", "phone")


@app.route("/users", methods=["GET"])
def get_users():
    users = session.execute(select(User)).scalars().all()
    return jsonify(
        [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
            }
            for user in users
        ]
    )


@app.route("/courses", methods=["GET"])
def get_courses():
    courses = session.execute(select(Course)).scalars().all()
    return jsonify(
        [
            {"id": course.id, "title": course.title, "teacher_id": course.teacher_id}
            for course in courses
        ]
    )


@app.route("/courses/create", methods=["GET", "POST"])
def create_course():
    if request.method == "POST":
        data = request.form
        course = Course(title=data["title"], teacher_id=data["teacher_id"])
        session.add(course)
        session.commit()
        return jsonify({"id": course.id, "title": course.title}), 201
    return create_form("title", "teacher_id")


@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = session.get(Course, course_id)
    if not course:
        return "Course not found", 404
    return jsonify(
        {
            "id": course.id,
            "title": course.title,
            "teacher_id": course.teacher_id,
            "students": [student.id for student in course.students],
            "lectures": [
                {"id": lecture.id, "title": lecture.title} for lecture in course.lessons
            ],
            "tasks": [
                {"id": task.id, "description": task.description}
                for task in course.homeworks
            ],
        }
    )


@app.route("/courses/<int:course_id>/lectures", methods=["GET", "POST"])
def manage_lectures(course_id):
    if request.method == "POST":
        data = request.form
        lecture = Lesson(
            title=data["title"], description=data["description"], course_id=course_id
        )
        session.add(lecture)
        session.commit()
        return jsonify({"id": lecture.id, "title": lecture.title}), 201
    return create_form("title", "description")


@app.route("/courses/<int:course_id>/tasks", methods=["GET", "POST"])
def manage_tasks(course_id):
    if request.method == "POST":
        data = request.form
        task = Homework(
            description=data["description"],
            max_score=data["max_score"],
            course_id=course_id,
        )
        session.add(task)
        session.commit()
        return jsonify({"id": task.id, "description": task.description}), 201
    return create_form("description", "max_score")


@app.route(
    "/courses/<int:course_id>/tasks/<int:task_id>/answers", methods=["GET", "POST"]
)
def manage_answers(course_id, task_id):
    if request.method == "POST":
        data = request.form
        answer = HomeworkResponse(
            description=data["description"],
            student_id=data["student_id"],
            homework_id=task_id,
        )
        session.add(answer)
        session.commit()
        return jsonify({"id": answer.id, "description": answer.description}), 201
    return create_form("description", "student_id")


@app.route(
    "/courses/<int:course_id>/tasks/<int:task_id>/answers/<int:answer_id>/mark",
    methods=["GET", "POST"],
)
def grade_answer(course_id, task_id, answer_id):
    if request.method == "POST":
        data = request.form
        grade = HomeworkGrade(
            date=data["date"],
            score=data["score"],
            teacher_id=data["teacher_id"],
            response_id=answer_id,
        )
        session.add(grade)
        session.commit()
        return jsonify({"id": grade.id, "score": grade.score}), 201
    return create_form("date", "score", "teacher_id")


@app.route("/courses/<int:course_id>/rating", methods=["GET"])
def get_course_rating(course_id):
    students = {}
    tasks = (
        session.execute(select(Homework).where(Homework.course_id == course_id))
        .scalars()
        .all()
    )
    for task in tasks:
        responses = (
            session.execute(
                select(HomeworkResponse).where(HomeworkResponse.homework_id == task.id)
            )
            .scalars()
            .all()
        )
        for response in responses:
            grades = (
                session.execute(
                    select(HomeworkGrade).where(
                        HomeworkGrade.response_id == response.id
                    )
                )
                .scalars()
                .all()
            )
            scores = [grade.score for grade in grades]
            if scores:
                if response.student_id not in students:
                    students[response.student_id] = []
                students[response.student_id].extend(scores)

    rating = [
        {"student_id": student_id, "average_score": sum(scores) / len(scores)}
        for student_id, scores in students.items()
    ]
    rating.sort(key=lambda x: x["average_score"], reverse=True)
    return jsonify(rating)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
