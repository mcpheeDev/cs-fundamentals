import sqlite3

# ── Schema ────────────────────────────────────────────────────────────────────

SCHEMA = """
-- TODO: write CREATE TABLE statements for:
--   departments (dept_id TEXT PRIMARY KEY, name, head)
--   courses     (course_id TEXT PRIMARY KEY, title, credits, dept_id FK)
--   students    (student_id TEXT PRIMARY KEY, first_name, last_name, email UNIQUE, dob)
--   enrollments (enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
--                student_id FK, course_id FK, grade REAL,
--                UNIQUE(student_id, course_id))
"""

# ── Seed data ─────────────────────────────────────────────────────────────────

def seed(conn):
    """TODO: insert at least 3 departments, 6 courses, 6 students, 15 enrollments."""
    pass


# ── Setup ─────────────────────────────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(":memory:")   # change to "students.db" to persist
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup(conn):
    conn.executescript(SCHEMA)
    seed(conn)


# ── Queries ───────────────────────────────────────────────────────────────────

def all_students(conn):
    """
    TODO: return all students as a list of rows, sorted by last_name.
    Each row should have at least: student_id, first_name, last_name, email.
    """
    pass


def courses_by_dept(conn, dept_id):
    """
    TODO: return all courses in the given department.
    Each row: course_id, title, credits.
    """
    pass


def student_report(conn, student_id):
    """
    TODO: return all enrollments for the student, joined with course info.
    Each row: course title, department name, grade.
    Order by grade descending.
    """
    pass


def average_by_course(conn):
    """
    TODO: return average grade and student count for every course.
    JOIN courses and departments.
    Order by average grade descending.
    """
    pass


def high_achievers(conn, min_avg=80):
    """
    TODO: return students whose average grade across all courses >= min_avg.
    Use HAVING to filter after GROUP BY.
    Each row: student name, average grade, number of courses taken.
    Order by average grade descending.
    """
    pass


def update_grade(conn, student_id, course_id, new_grade):
    """
    TODO: update the grade for a specific enrollment.
    Commit the change.
    Return True if a row was updated, False if the enrollment wasn't found.
    """
    pass


def enroll(conn, student_id, course_id, grade=None):
    """
    TODO: insert a new enrollment.
    Return True on success.
    Return False (don't raise) if the student is already enrolled.
    """
    pass


def department_summary(conn):
    """
    TODO: for each department return:
      - department name and head
      - number of courses
      - number of distinct enrolled students
      - overall average grade
    Use LEFT JOINs so departments with no students still appear.
    """
    pass


# ── CLI (bonus) ───────────────────────────────────────────────────────────────

def run_cli(conn):
    """
    TODO (bonus): build a simple interactive CLI.
    Commands: students, courses <dept>, report <id>, top, quit
    """
    pass


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    conn = get_connection()
    setup(conn)

    print("All students:")
    for row in (all_students(conn) or []):
        print(f"  [{row['student_id']}] {row['first_name']} {row['last_name']}")

    print("\nHigh achievers (avg >= 80%):")
    for row in (high_achievers(conn) or []):
        print(f"  {row[0]}  avg={row[1]}%")

    print("\nDepartment summary:")
    for row in (department_summary(conn) or []):
        print(f"  {row[0]}")

    conn.close()
