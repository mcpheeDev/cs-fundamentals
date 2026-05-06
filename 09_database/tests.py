from app import (get_connection, setup, all_students, courses_by_dept,
                  student_report, average_by_course, high_achievers,
                  update_grade, enroll)

passed = 0
failed = 0

def test(name, got, expected):
    global passed, failed
    if got == expected:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  {name}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")
        failed += 1

def test_true(name, condition):
    test(name, condition, True)


conn = get_connection()
setup(conn)

print("\n── Schema ────────────────────────────────────────────")
tables = {r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
for t in ("departments", "courses", "students", "enrollments"):
    test_true(f"table '{t}' exists", t in tables)

fk_on = conn.execute("PRAGMA foreign_keys").fetchone()[0]
test("foreign keys enabled", fk_on, 1)

print("\n── Seed data ─────────────────────────────────────────")
dept_count    = conn.execute("SELECT COUNT(*) FROM departments").fetchone()[0]
course_count  = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
enroll_count  = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]

test_true("at least 3 departments", dept_count >= 3)
test_true("at least 6 courses",     course_count >= 6)
test_true("at least 6 students",    student_count >= 6)
test_true("at least 15 enrollments", enroll_count >= 15)

print("\n── all_students ──────────────────────────────────────")
students = all_students(conn)
test_true("returns a list", isinstance(students, list))
test_true("returns all students", len(students) >= 6)
# Check sorted by last name
names = [r['last_name'] for r in students]
test("sorted by last name", names, sorted(names))

print("\n── courses_by_dept ───────────────────────────────────")
first_dept = conn.execute("SELECT dept_id FROM departments LIMIT 1").fetchone()[0]
courses = courses_by_dept(conn, first_dept)
test_true("returns a list", isinstance(courses, list))
test_true("returns at least 1 course", len(courses) >= 1)

print("\n── student_report ────────────────────────────────────")
first_student = conn.execute(
    "SELECT student_id FROM students LIMIT 1").fetchone()[0]
report = student_report(conn, first_student)
test_true("returns a list", isinstance(report, list))
test_true("student has at least 1 enrollment", len(report) >= 1)

print("\n── average_by_course ─────────────────────────────────")
avgs = average_by_course(conn)
test_true("returns a list", isinstance(avgs, list))
test_true("covers multiple courses", len(avgs) >= 3)

print("\n── high_achievers ────────────────────────────────────")
achievers = high_achievers(conn, min_avg=0)   # 0 = all students qualify
test_true("returns a list", isinstance(achievers, list))
test_true("returns at least 1 student", len(achievers) >= 1)

achievers_80 = high_achievers(conn, min_avg=999)  # nobody qualifies
test("min_avg=999 returns empty list", achievers_80, [])

print("\n── update_grade ──────────────────────────────────────")
first_enroll = conn.execute(
    "SELECT student_id, course_id FROM enrollments LIMIT 1").fetchone()
sid, cid = first_enroll
result = update_grade(conn, sid, cid, 99.0)
test("returns True on success", result, True)
new_grade = conn.execute(
    "SELECT grade FROM enrollments WHERE student_id=? AND course_id=?",
    (sid, cid)).fetchone()[0]
test("grade was actually updated", new_grade, 99.0)

result_bad = update_grade(conn, "FAKE_ID", "FAKE_COURSE", 50)
test("returns False for missing enrollment", result_bad, False)

print("\n── enroll ────────────────────────────────────────────")
# get a student and a course they're NOT enrolled in
all_pairs = {(r[0], r[1]) for r in conn.execute(
    "SELECT student_id, course_id FROM enrollments").fetchall()}
all_sids = [r[0] for r in conn.execute("SELECT student_id FROM students").fetchall()]
all_cids = [r[0] for r in conn.execute("SELECT course_id FROM courses").fetchall()]

new_pair = None
for s in all_sids:
    for c in all_cids:
        if (s, c) not in all_pairs:
            new_pair = (s, c)
            break
    if new_pair:
        break

if new_pair:
    result = enroll(conn, new_pair[0], new_pair[1], grade=75)
    test("enroll returns True", result, True)
    exists = conn.execute(
        "SELECT 1 FROM enrollments WHERE student_id=? AND course_id=?",
        new_pair).fetchone()
    test_true("enrollment was inserted", exists is not None)

    result2 = enroll(conn, new_pair[0], new_pair[1], grade=75)
    test("duplicate enroll returns False", result2, False)

conn.close()

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
