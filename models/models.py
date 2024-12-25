from sqlalchemy import Column, String, ForeignKey, Text, Date, Float, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


course_student_association = Table(
    "course_students",
    Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)

    taught_courses = relationship(
        "Course", back_populates="teacher", cascade="all, delete-orphan"
    )
    enrolled_courses = relationship(
        "Course", secondary=course_student_association, back_populates="students"
    )


class Course(Base):
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    teacher = relationship("User", back_populates="taught_courses")
    students = relationship(
        "User", secondary=course_student_association, back_populates="enrolled_courses"
    )
    lessons = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan"
    )
    homeworks = relationship(
        "Homework", back_populates="course", cascade="all, delete-orphan"
    )


class Lesson(Base):
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    course = relationship("Course", back_populates="lessons")


class Homework(Base):
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    max_score: Mapped[float] = mapped_column(Float, nullable=False)

    course = relationship("Course", back_populates="homeworks")
    responses = relationship(
        "HomeworkResponse", back_populates="homework", cascade="all, delete-orphan"
    )


class HomeworkResponse(Base):
    homework_id: Mapped[int] = mapped_column(ForeignKey("homeworks.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    homework = relationship("Homework", back_populates="responses")
    student = relationship("User")
    grades = relationship(
        "HomeworkGrade", back_populates="response", cascade="all, delete-orphan"
    )


class HomeworkGrade(Base):
    response_id: Mapped[int] = mapped_column(
        ForeignKey("homeworkresponses.id"), nullable=False
    )
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    response = relationship("HomeworkResponse", back_populates="grades")
    teacher = relationship("User")
