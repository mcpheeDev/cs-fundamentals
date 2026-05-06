"""
app.py — A full student records database application.

Schema (3NF normalised):
  students    (student_id, first_name, last_name, email, dob)
  courses     (course_id, title, credits, dept_id)
  departments (dept_id, name, head)
  enrollments (enrollment_id AUTOINCREMENT, student_id, course_id, grade)

Demonstrates: CREATE, INSERT, SELECT, WHERE, JOIN, GROUP BY,
              ORDER BY, UPDATE, DELETE, aggregate functions.

Run:  python3 app.py
"""

import sqlite3
from datetime import datetime

SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    dept_id TEXT PRIMARY KEY,
    name    TEXT NOT NULL,
    head    TEXT
);
CREATE TABLE IF NOT EXISTS courses (
    course_id TEXT PRIMARY KEY,
    title     TEXT NOT NULL,
    credits   INTEGER NOT NULL,
    dept_id   TEXT NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    dob        TEXT
);
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id    TEXT NOT NULL,
    course_id     TEXT NOT NULL,
    grade         REAL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id),
    UNIQUE (student_id, course_id)
);
"""

DEPTS = [
    ("CS",   "Computer Science", "Prof. Alan Turing"),
    ("MATH", "Mathematics",      "Prof. Emmy Noether"),
    ("PHYS", "Physics",          "Prof. Marie Curie"),
]
COURSES = [
    ("CS101",   "Intro to Programming",  30, "CS"),
    ("CS201",   "Data Structures",       30, "CS"),
    ("CS301",   "Algorithms",            30, "CS"),
    ("CS401",   "Machine Learning",      30, "CS"),
    ("MATH101", "Calculus I",            30, "MATH"),
    ("MATH201", "Linear Algebra",        30, "MATH"),
    ("PHYS101", "Classical Mechanics",   30, "PHYS"),
]
STUDENTS = [
    ("S001","Alice","Chen",  "alice@uni.ac.uk","2004-03-15"),
    ("S002","Bob",  "Smith", "bob@uni.ac.uk",  "2003-11-02"),
    ("S003","Carol","Jones", "carol@uni.ac.uk","2004-07-21"),
    ("S004","Dave", "Wilson","dave@uni.ac.uk", "2003-09-08"),
    ("S005","Eve",  "Taylor","eve@uni.ac.uk",  "2004-01-30"),
    ("S006","Frank","Brown", "frank@uni.ac.uk","2003-06-14"),
]
ENROLLMENTS = [
    ("S001","CS101",78), ("S001","CS201",85),  ("S001","MATH101",91),
    ("S002","CS101",62), ("S002","CS201",55),  ("S002","CS301",70),
    ("S003","CS101",88), ("S003","MATH101",94),("S003","MATH201",89),
    ("S004","CS101",45), ("S004","PHYS101",73),("S004","MATH101",68),
    ("S005","CS101",95), ("S005","CS201",92),  ("S005","CS301",88),
    ("S005","CS401",97),
    ("S006","PHYS101",81),("S006","MATH101",76),("S006","MATH201",72),
]


def setup(conn):
    conn.executescript(SCHEMA)
    conn.executemany("INSERT OR IGNORE INTO departments VALUES (?,?,?)", DEPTS)
    conn.executemany("INSERT OR IGNORE INTO courses    VALUES (?,?,?,?)", COURSES)
    conn.executemany("INSERT OR IGNORE INTO students   VALUES (?,?,?,?,?)", STUDENTS)
    conn.executemany(
        "INSERT OR IGNORE INTO enrollments (student_id,course_id,grade) VALUES (?,?,?)",
        ENROLLMENTS)
    conn.commit()


def q1_all_students(conn):
    print("\n── Q1: All students ─────────────────────────────")
    rows = conn.execute(
        "SELECT student_id, first_name||' '||last_name AS name, email "
        "FROM students ORDER BY last_name").fetchall()
    for r in rows:
        print(f"  [{r[0]}]  {r[1]:<20}  {r[2]}")


def q2_cs_courses(conn):
    print("\n── Q2: Computer Science courses ─────────────────")
    rows = conn.execute(
        "SELECT course_id, title, credits FROM courses "
        "WHERE dept_id='CS' ORDER BY course_id").fetchall()
    for r in rows:
        print(f"  {r[0]:<10}  {r[1]:<30}  {r[2]} credits")


def q3_student_grades(conn, student_id="S005"):
    print(f"\n── Q3: Grade report for {student_id} ────────────────")
    rows = conn.execute("""
        SELECT s.first_name||' '||s.last_name, c.title, e.grade
        FROM   enrollments e
        JOIN   students s ON e.student_id=s.student_id
        JOIN   courses  c ON e.course_id=c.course_id
        WHERE  e.student_id=?
        ORDER  BY e.grade DESC""", (student_id,)).fetchall()
    for r in rows:
        bar = "█" * int(r[2] / 10) + "░" * (10 - int(r[2] / 10))
        print(f"  {r[1]:<35}  [{bar}] {r[2]:.0f}%")


def q4_avg_by_course(conn):
    print("\n── Q4: Average grade per course ─────────────────")
    rows = conn.execute("""
        SELECT c.title, d.name, ROUND(AVG(e.grade),1), COUNT(e.student_id)
        FROM   enrollments e
        JOIN   courses     c ON e.course_id=c.course_id
        JOIN   departments d ON c.dept_id=d.dept_id
        GROUP  BY e.course_id ORDER BY 3 DESC""").fetchall()
    for r in rows:
        print(f"  {r[0]:<35}  {r[1]:<20}  avg={r[2]}%  n={r[3]}")


def q5_high_achievers(conn):
    print("\n── Q5: High achievers (avg ≥ 80%) ──────────────")
    rows = conn.execute("""
        SELECT s.first_name||' '||s.last_name,
               ROUND(AVG(e.grade),1), COUNT(e.course_id)
        FROM   enrollments e
        JOIN   students s ON e.student_id=s.student_id
        GROUP  BY e.student_id
        HAVING AVG(e.grade)>=80
        ORDER  BY 2 DESC""").fetchall()
    for r in rows:
        print(f"  {r[0]:<20}  avg={r[1]}%  courses={r[2]}")


def q6_update_grade(conn):
    print("\n── Q6: Update a grade ────────────────────────────")
    old = conn.execute(
        "SELECT grade FROM enrollments WHERE student_id='S002' AND course_id='CS201'"
    ).fetchone()
    print(f"  Before: {old[0]}%")
    conn.execute(
        "UPDATE enrollments SET grade=72 WHERE student_id='S002' AND course_id='CS201'")
    conn.commit()
    new = conn.execute(
        "SELECT grade FROM enrollments WHERE student_id='S002' AND course_id='CS201'"
    ).fetchone()
    print(f"  After:  {new[0]}%  ✓")


def q7_dept_summary(conn):
    print("\n── Q7: Department summary ────────────────────────")
    rows = conn.execute("""
        SELECT d.name, d.head,
               COUNT(DISTINCT c.course_id),
               COUNT(DISTINCT e.student_id),
               ROUND(AVG(e.grade),1)
        FROM   departments d
        LEFT JOIN courses     c ON d.dept_id=c.dept_id
        LEFT JOIN enrollments e ON c.course_id=e.course_id
        GROUP  BY d.dept_id ORDER BY 5 DESC""").fetchall()
    for r in rows:
        print(f"  {r[0]:<20}  {r[1]:<28}  "
              f"courses={r[2]}  students={r[3]}  avg={r[4]}%")


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    setup(conn)
    print("╔══════════════════════════════════════════╗")
    print("║       Student Records Database           ║")
    print("╚══════════════════════════════════════════╝")
    q1_all_students(conn)
    q2_cs_courses(conn)
    q3_student_grades(conn)
    q4_avg_by_course(conn)
    q5_high_achievers(conn)
    q6_update_grade(conn)
    q7_dept_summary(conn)
    conn.close()
    print("\n  Done.\n")
