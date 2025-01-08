from datetime import datetime
import random
import string

from flask import Flask, request, redirect, render_template, url_for
from sqlalchemy import select

from form import create_form
from models import Course, Lesson, User, Homework, HomeworkResponse, HomeworkGrade
from database import session


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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
        return redirect(url_for("get_users"))
    form = create_form("email", "password", "first_name", "last_name", "phone")
    return render_template("register.html", form=form)


@app.route("/users", methods=["GET"])
def get_users():
    users = session.execute(select(User)).scalars().all()
    return render_template("users.html", users=users)


@app.route("/courses", methods=["GET"])
def get_courses():
    courses = session.execute(select(Course)).scalars().all()
    return render_template("courses.html", courses=courses)


@app.route("/courses/create", methods=["GET", "POST"])
def create_course():
    if request.method == "POST":
        data = request.form
        course = Course(title=data["title"], teacher_id=data["teacher_id"])
        session.add(course)
        session.commit()
        return redirect(url_for("get_courses"))
    form = create_form("title", "teacher_id")
    return render_template("create_course.html", form=form)


@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = session.get(Course, course_id)
    if not course:
        return "Course not found", 404
    return render_template("course_details.html", course=course)


@app.route("/courses/<int:course_id>/lectures", methods=["GET", "POST"])
def manage_lectures(course_id):
    if request.method == "POST":
        data = request.form
        lecture = Lesson(
            title=data["title"], description=data["description"], course_id=course_id
        )
        session.add(lecture)
        session.commit()
        return redirect(url_for("manage_lectures", course_id=course_id))
    lectures = (
        session.execute(select(Lesson).where(Lesson.course_id == course_id))
        .scalars()
        .all()
    )
    form = create_form("title", "description")
    return render_template("add_lecture.html", lectures=lectures, form=form)


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
        return redirect(url_for("manage_tasks", course_id=course_id))
    tasks = (
        session.execute(select(Homework).where(Homework.course_id == course_id))
        .scalars()
        .all()
    )
    form = create_form("description", "max_score")
    return render_template("add_task.html", tasks=tasks, form=form)


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
        return redirect(url_for("manage_answers", course_id=course_id, task_id=task_id))
    answers = (
        session.execute(
            select(HomeworkResponse).where(HomeworkResponse.homework_id == task_id)
        )
        .scalars()
        .all()
    )
    form = create_form("description", "student_id")
    return render_template("add_answer.html", answers=answers, form=form)


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
        return redirect(
            url_for(
                "grade_answer",
                course_id=course_id,
                task_id=task_id,
                answer_id=answer_id,
            )
        )
    grades = (
        session.execute(
            select(HomeworkGrade).where(HomeworkGrade.response_id == answer_id)
        )
        .scalars()
        .all()
    )
    form = create_form("date", "score", "teacher_id")
    return render_template("grade_answer.html", grades=grades, form=form)


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
    return render_template("rating.html", rating=rating)


if __name__ == "__main__":
    app.run(debug=True)
