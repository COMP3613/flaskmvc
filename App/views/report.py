from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from .index import index_views

from App.controllers import (
    get_all_reports,
    get_all_reports_json,
    create_report,
    get_student_reports_json,
    update_report,
    delete_report
)

report_views = Blueprint('report_views', __name__, template_folder='../templates')


@report_views.route('/api/report/list', methods=['GET'])
@jwt_required()
def view_all_reports():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    reports, code = get_all_reports_json()
    return jsonify(reports.get_json()), code


@report_views.route('/api/report/add', methods=['POST'])
@jwt_required()
def create_report_action():
    if jwt_current_user.type != "staff":
        return jsonify({"error": "You must be logged into a staff account to do this"}), 403

    data = request.json
    student_id = int(data['student_id'])
    staff_id = int(data['staff_id'])
    review = data['review']
    rating = int(data['rating'])
    
    if not student_id or not staff_id or not review or not rating:
        return jsonify({"error": "Missing required fields"}), 400

    result, code = create_report(student_id, staff_id, review, rating)

    return (jsonify({"message": f"{result}"}) if code == 201 else jsonify({"error": result}), code)


@report_views.route('/api/report/search-id', methods=['GET'])
@jwt_required()
def get_searchstudent_route():
    student_id = request.args.get('student_id')
    
    if not student_id:
        return jsonify({"error":"Student ID field is empty"}),400

    try:
        student_id = int(student_id)
    except ValueError:
        return jsonify({"error": "Invalid Student ID"}), 400
        
    result,code = get_student_reports_json(student_id)
    
    if result == []:
        return jsonify({"error": "No reports found for this student"}), 404
    return jsonify(result.get_json()), code


@report_views.route('/api/report/delete', methods=['DELETE'])
@jwt_required()
def delete_searchstudent():
    report = request.json
    try:
        report = int(report.get('report_id'))
    except ValueError:
        return jsonify({"error": "Invalid Report ID"}), 400

    result,code = delete_report(report)
    return (jsonify({"message": result}) if code == 200 else jsonify({"error": result}), code)

@report_views.route('/api/report/update', methods=['POST'])
@jwt_required()
def update_report_route():
    data = request.json

    if 'report_id' not in data or 'review' not in data or 'rating' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        report_id = int(data['report_id'])
        rating = int(data['rating'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid report ID or rating"}), 400


    student_id = data.get('student_id')
    if student_id == '':
        student_id = None
    else:
        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid student ID"}), 400


    result = update_report(report_id, data['review'], rating, student_id)


    if "not found" in result.lower():
        return jsonify({"error": result}), 404 

    return jsonify({"message": f"{result}"}), 200  
