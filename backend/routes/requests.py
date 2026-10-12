from flask import Blueprint, jsonify, request

from backend.services import student_service
from backend.services.filters import parse_query_filters, parse_body_filters

from backend.utils.exception import BadRequestError

requests_bp=Blueprint("requests", __name__)

def get_json_body():
    if not request.is_json:
        raise BadRequestError("тело запроса не джисон")
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequestError("не точный джисон")
    return data

@requests_bp.route("/api/requests", methods=["GET"])
def get_requests():
    filters=parse_query_filters(request.args)
    students=student_service.get_students(filters)
    return jsonify(students),200


@requests_bp.route("/api/requests/<int:isu_id>", methods=["GET"])
def get_request(isu_id):
    student=student_service.get_student(isu_id)
    return jsonify(student),200

@requests_bp.route("/api/requests", methods=["POST"])
def create_request():
    data=get_json_body()
    student=student_service.create_student(data)
    return jsonify(student),201

@requests_bp.route("/api/requests/<int:isu_id>", methods=["PATCH"])
def patch_request(isu_id):
    data=get_json_body()
    student=student_service.update_student(isu_id, data)
    return jsonify(student),200

@requests_bp.route("/api/requests/<int:isu_id>", methods=["DELETE"])
def delete_request(isu_id):
    student_service.delete_student(isu_id)
    return "",204

@requests_bp.route("/api/requests", methods=["QUERY"])
def query_requests():
    data=get_json_body()
    filters=parse_body_filters(data)
    students=student_service.get_students(filters)
    return jsonify(students),200




