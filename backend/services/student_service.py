from datetime import datetime

from backend.models.student import Student
from backend.repositories import student_repository
from backend.utils.exception import ValidationError, NotFoundError, ConflictError


REQUIRED_FIELDS = [
    "fullName",
    "group",
    "isuId",
    "dormNumber",
    "room",
    "moveInDate",
    "isForeigner"
]

ALLOWED_FIELDS = {
    "fullName",
    "group",
    "isuId",
    "dormNumber",
    "room",
    "moveInDate",
    "isForeigner",
    "notes",
}

IMMUTABLE_ON_PATCH = {"isuId"}
def validate_student_data(data, is_patch=False):
    errors = {}

    if not isinstance(data, dict):
        return {"body": "JSON должен быть объектом"}
    for field in data:
        if field not in ALLOWED_FIELDS:
            errors[field] = "Неизвестное поле"

    if not is_patch:
        for field in REQUIRED_FIELDS:
            if field not in data:
                errors[field] = "Поле обязательно"
    if is_patch:
        for field in IMMUTABLE_ON_PATCH:
            if field in data:
                errors[field] = "Это поле является идентификатором и не может быть изменено"

    if "fullName" in data:
        full_name = data["fullName"]
        if not isinstance(full_name, str) or not full_name.strip():
            errors["fullName"] = "ФИО не может быть пустым"
        elif any(ch.isdigit() for ch in full_name):
            errors["fullName"] = "ФИО не должно содержать цифры"

    if "group" in data:
        group = data["group"]

        if not isinstance(group, str):
            errors["group"] = "Группа должна быть строкой"
        elif len(group) != 5 or not group[0].isalpha() or not group[1:].isdigit():
            errors["group"] = "Группа должна иметь формат: 1 буква + 4 цифры"

    if "isuId" in data:
        if not isinstance(data["isuId"], int) or isinstance(data["isuId"], bool):
            errors["isuId"] = "ИСУ ID должен быть целым числом"
        elif data["isuId"] <= 0:
            errors["isuId"] = "ИСУ ID должен быть положительным"

    if "dormNumber" in data:
        if not isinstance(data["dormNumber"], int) or isinstance(data["dormNumber"], bool):
            errors["dormNumber"] = "Номер общежития должен быть целым числом"
        elif data["dormNumber"] <= 0:
            errors["dormNumber"] = "Номер общежития должен быть положительным"

    if "room" in data:
        if not isinstance(data["room"], int) or isinstance(data["room"], bool):
            errors["room"] = "Номер комнаты должен быть целым числом"
        elif data["room"] <= 0:
            errors["room"] = "Номер комнаты должен быть положительным"

    if "moveInDate" in data:
        date_value = data["moveInDate"]

        if not isinstance(date_value, str):
            errors["moveInDate"] = "Дата должна быть строкой"
        else:
            try:
                datetime.strptime(date_value, "%Y-%m-%d")
            except ValueError:
                errors["moveInDate"] = "Дата должна быть в формате YYYY-MM-DD"

    if "isForeigner" in data:
        if not isinstance(data["isForeigner"], bool):
            errors["isForeigner"] = "Поле должно иметь значение true или false"

    if "notes" in data:
        if not isinstance(data["notes"], str):
            errors["notes"] = "Заметки должны быть строкой"
    return errors

def _student_matches(student, filters):
    for key, value in filters.items():
        if key not in student:
            return False
        student_value = student[key]
        if key == "fullName":
            if str(value).lower() not in student_value.lower():
                return False
        elif str(student_value).lower() != str(value).lower():
            return False
    return True

def get_students(filters=None):
    students = student_repository.get_all_students()
    if not filters:
        return students
    return[s for s in students if _student_matches(s,filters)]


def get_student(isu_id):
    student=student_repository.get_student_by_isu_id(isu_id)
    if student is None:
        raise NotFoundError("студент не найден")
    return student


def create_student(data):
    errors = validate_student_data(data)
    if errors:
       raise ValidationError("Ошибка валидации", errors)
    if student_repository.get_student_by_isu_id(data["isuId"]):
        raise ConflictError("Конфликт данных",
                            {"isuId":"Студент с таким ИСУ ID уде сущетсвует"})

    student = Student(
        fullName=data["fullName"].strip(),
        group=data["group"].strip(),
        isuId=data["isuId"],
        dormNumber=data["dormNumber"],
        room=data["room"],
        moveInDate=data["moveInDate"],
        isForeigner=data["isForeigner"],
        notes=data.get("notes", "")
    )

    student_dict = student.to_dict()
    student_repository.add_student(student_dict)
    return student_dict


def update_student(isu_id, data):
    old_student = student_repository.get_student_by_isu_id(isu_id)
    if old_student is None:
        raise NotFoundError("студент не найден")
    errors = validate_student_data(data, is_patch=True)
    if errors:
        raise ValidationError("ошибка валидации", errors)
    updated_student = old_student.copy()
    for key in data:
        updated_student[key] = data[key]
    if "fullName" in updated_student:
        updated_student["fullName"] = updated_student["fullName"].strip()
    if "group" in updated_student:
        updated_student["group"] = updated_student["group"].strip()
    student_repository.update_student(isu_id, updated_student)
    return updated_student


def delete_student(isu_id):
    if not student_repository.delete_student(isu_id):
        raise NotFoundError("студенты не найдены")