ALTER TABLE user
    ADD COLUMN phone_number VARCHAR(20);

ALTER TABLE user
    DROP COLUMN dog_name;

ALTER TABLE homework
    ADD COLUMN deadline DATE;


ALTER TABLE homework_submission
    ADD COLUMN submission_date DATE;

CREATE TABLE homework_grade (
    id SERIAL PRIMARY KEY,
    submission_id INT REFERENCES homework_submission(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    grade INT NOT NULL,
    teacher_id INT REFERENCES user(id) ON DELETE CASCADE
);
