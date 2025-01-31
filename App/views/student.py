from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.student import *

from .index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')


@student_views.route('/api/student/list', methods=['GET'])
def list_students_route():
    students = get_all_students_json()
    return students


@student_views.route('/api/student/update', methods=['POST'])
@jwt_required()
def update_student_route():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    data = request.json
    student_id = data.get('student_id')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    if not student_id or not firstname or not lastname:
        return jsonify({"error": "Missing required fields"}), 400

    result, status_code = update_student(student_id, firstname, lastname)
    if status_code == 404:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student updated successfully"}), status_code


@student_views.route('/api/student/create', methods=['POST'])
@jwt_required()
def create_student_route():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    data = request.json
    student_id = data.get('student_id')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    if not student_id or not firstname or not lastname:
        return jsonify({"error": "Missing required fields"}), 400

    student, code = get_student_by_id(student_id)
    if code == 200:
        return jsonify({"error": "Student already exists"}), 422

    result, status_code = create_student(student_id, firstname, lastname)

    return jsonify({"message": "Student created successfully"}), status_code


@student_views.route('/api/student/delete', methods=['DELETE'])
@jwt_required()
def delete_student_route():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403
    student_id = request.json.get('student_id')
    if not student_id:
        return jsonify({"error": "Missing required fields"}), 400
    result, status_code = delete_student(student_id)

    if status_code == 404:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student deleted successfully"}), 200
