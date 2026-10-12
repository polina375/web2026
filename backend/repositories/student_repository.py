import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "students.json"

def get_all_students():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,"r", encoding="utf-8") as file:
        return json.load(file)

def save_all_students(students):
    with open(DATA_FILE,"w", encoding="utf-8") as file:
        json.dump(students, file, ensure_ascii=False, indent=2)


def get_student_by_isu_id(isu_id):
    students = get_all_students()
    for student in students:
        if student["isuId"]==isu_id:
            return student
    return None


def add_student(student):
    students = get_all_students()
    students.append(student)
    save_all_students(students)


def update_student(isu_id, new_data):
    students = get_all_students()
    for i in range(len(students)):
        if students[i]["isuId"] == isu_id:
            students[i] = new_data
            save_all_students(students)
            return True
    return False


def delete_student(isu_id):
    students = get_all_students()
    new_students = [s for s in students if s["isuId"]!=isu_id]
    if len(new_students) == len(students):
        return False
    save_all_students(new_students)
    return True
