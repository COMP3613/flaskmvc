from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    get_all_reports,
    get_all_reports_json,
    create_report,
    get_student_reports_json,
    update_report,
    delete_report
)

report_views = Blueprint('report_views', __name__, template_folder='../templates')

@report_views.route('/api/report/list', methods = ['GET'])
def view_all_reports():
    reports = get_all_reports_json('asc')
    return jsonify(reports)

@report_views.route('/api/report/add', methods=['POST'])
def create_report_action():
    data=request.json
    student_id = int(data['student_id'])
    staff_id = int(data['staff_id'])
    review = data['review']
    rating = int(data['rating'])
    result = create_report(student_id, staff_id, review, rating)
    reports = get_all_reports_json('asc')
    return jsonify({"message" : f"{result}"},
                   {"reports" : f"{reports}"})


@report_views.route('/api/report/search-id', methods=['GET'])
def get_searchstudent_page():
    student_id = request.args.get('student_id')
    student_id = int(student_id)
    result = get_student_reports_json(student_id)
    return jsonify({"query-result" : f"{result}"}) 



@report_views.route('/api/report/delete', methods=['POST'])
def delete_searchstudent():
    report = request.args.get('report_id')
    report = int(report)
    result = delete_report(int(report))
    reports = get_all_reports('asc')
    return jsonify({"message" : f"{result}"},
                   {"reports" : f"{reports}"})


@report_views.route('/api/report/update', methods=['POST'])
def update_report_page():
    data=request.json
    report_id = int(data['report_id'])
    rating = int(data['rating'])
    reports = get_all_reports('asc')
    if data['student_id'] == '':
        result = update_report(report_id, data['review'], rating, None)
        return jsonify({'message' : f"{result}"},
                   {"reports" : f"{reports}"})
    student_id = int(data['student_id'])
    result = update_report(report_id, data['review'], rating, student_id)
    return jsonify({"message" : f"{result}"},
                   {"reports" : f"{reports}"})  

   

