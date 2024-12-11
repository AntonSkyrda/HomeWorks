CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dog_name VARCHAR(100),
    photo BYTEA
);

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    teacher_id INT REFERENCES user(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE course_student (
    course_id INT REFERENCES course(id) ON DELETE CASCADE,
    student_id INT REFERENCES user(id) ON DELETE CASCADE,
    PRIMARY KEY (course_id, student_id)
);

CREATE TABLE lesson (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES course(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE homework (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES course(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    max_grade INT NOT NULL
);

CREATE TABLE homework_submission (
    id SERIAL PRIMARY KEY,
    homework_id INT REFERENCES homework(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    student_id INT REFERENCES user(id) ON DELETE CASCADE,
    grade INT
);
