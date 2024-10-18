from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.staff import (get_all_staff, get_all_staff_json, create_staff, get_staff_by_id,
                                   get_staff_by_username, delete_staff)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


@staff_views.route('/api/staff/list', methods=['GET'])
@jwt_required()
def list_staff_route():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    staff, code = get_all_staff_json()
    return jsonify(staff), code


@staff_views.route('/api/staff/create', methods=['PUT'])
@jwt_required()
def create_staff_route():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    data = request.json
    username = data.get('username')
    password = data.get('password')
    department = data.get('department')
    faculty = data.get('faculty')

    if not username or not password or not department or not faculty:
        return jsonify({"error": "Missing required fields"}), 400

    staff, code = get_staff_by_username(username)
    if code == 200:
        return jsonify({"error": "Staff already exists"}), 422

    result = create_staff(username, password, department, faculty).get_json()
    return result, 201


@staff_views.route('/api/staff/delete', methods=['DELETE'])
@jwt_required()
def delete_staff_route():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    staff_id = request.args.get('staff_id')
    if not staff_id:
        return jsonify({"error": "Staff ID is required"}), 400

    try:
        staff_id = int(staff_id)
    except ValueError:
        return jsonify({"error": "Invalid Staff ID"}), 400

    result = delete_staff(staff_id)
    if "not found" in result:
        return jsonify({"error": result}), 404

    return jsonify({"message": result}), 200
