# 09 – Student Database

## What you're building
A fully functional student records system backed by SQLite.
You write the schema, seed the data, and implement all the queries.

## Part 1 — Schema (`app.py`)
Design a normalised database with these four tables:

```
departments  (dept_id, name, head)
courses      (course_id, title, credits, dept_id → departments)
students     (student_id, first_name, last_name, email, dob)
enrollments  (enrollment_id AUTOINCREMENT, student_id → students,
              course_id → courses, grade)
```

All foreign keys must be enforced. `enrollments` should have a UNIQUE
constraint on (student_id, course_id) — a student can only enroll once.

## Part 2 — Seed data
Insert at least:
- 3 departments
- 6 courses (spread across departments)
- 6 students
- 15+ enrollments with grades

## Part 3 — Queries to implement

| Function | What it does | SQL features used |
|----------|-------------|------------------|
| `all_students()` | List all students sorted by last name | SELECT, ORDER BY |
| `courses_by_dept(dept_id)` | List courses in a department | SELECT, WHERE |
| `student_report(student_id)` | Full grade report for one student | JOIN, ORDER BY |
| `average_by_course()` | Average grade per course | JOIN, GROUP BY, AVG |
| `high_achievers(min_avg)` | Students averaging above min_avg | GROUP BY, HAVING |
| `update_grade(sid, cid, grade)` | Update a specific grade | UPDATE |
| `enroll(student_id, course_id)` | Enroll student in course | INSERT |
| `department_summary()` | Stats per department | Multi-table JOIN, AVG |

## Part 4 — CLI (bonus)
Wrap everything in a simple command-line interface that lets you
call each function interactively.

## Run tests
```bash
python3 tests.py
```
