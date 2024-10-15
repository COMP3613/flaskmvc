import click, pytest, sys
from flask import Flask, jsonify, request
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Staff, Student, Report
from App.main import create_app
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)
current_user = None


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')


# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="table")
def list_user_command(format):
    users = get_all_users()
    if format == 'table':
        print("ID | Username")
        print("--------------")
        for user in users:
            print(f"{user.id:2d} | {user.username}")
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')


@staff_cli.command("create", help="Creates a staff member account")
@click.argument("username", default="Josh")
@click.argument("password", default="joshpass")
@click.argument("department", default="DCIT")
@click.argument("faculty", default="FST")
def create_staff_command(username, password, department, faculty):
    create_staff(username, password, department, faculty)
    print(f'{username} created as a staff member!')


@staff_cli.command("delete", help="Deletes an existing staff member")
def delete_staff_command():
    staff_members = get_all_staff()
    if not staff_members:
        print("No staff members found.")
        return

    print("Select a staff member to delete:")
    for index, staff in enumerate(staff_members, start=1):
        print(f"{index}\t{staff.username}\t(ID: {staff.id})")

    selected_index = input("Enter the number of the staff member you want to delete: ")
    if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(staff_members):
        print("Invalid selection. Please try again.")
        return

    selected_staff = staff_members[int(selected_index) - 1]
    confirm = input(
        f"Are you sure you want to delete staff member {selected_staff.username} (ID: {selected_staff.id})? (y/n): ")

    if confirm.lower() == 'y':
        result = delete_staff(selected_staff.id)
        print(f"{result}")


@staff_cli.command("create_report", help="Creates a report for a given student")
def create_report_command():
    students, code = get_all_students()
    if not students:
        print("No students found.")
        return

    print("Select a student:")
    for index, student in enumerate(students, start=1):
        print(f"{index}\t{student.firstname}\t{student.lastname}")

    selected_index = input("Enter the number of the student you want to report on: ")
    if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(students):
        print("Invalid selection. Please try again.")
        return

    selected_student = students[int(selected_index) - 1]

    staff_members, code = get_all_staff()
    if not staff_members:
        print("No staff members found.")
        return

    print("Select a staff member:")
    for index, staff in enumerate(staff_members, start=1):
        print(f"{index}\t{staff.username}")

    selected_staff_index = input("Enter the number of the staff member rating the report: ")
    if not selected_staff_index.isdigit() or int(selected_staff_index) < 1 or int(selected_staff_index) > len(
            staff_members):
        print("Invalid selection. Please try again.")
        return

    selected_staff = staff_members[int(selected_staff_index) - 1]

    report = input("Please enter the report for the given student: ")
    rating = input("Please enter a rating (1-5): ")

    if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        print("Invalid rating. Rating must be between 1 and 5.")
        return

    result = create_report(selected_student.id, selected_staff.id, report, int(rating))
    print(result)


@staff_cli.command("update_report", help="Updates an existing report")
def update_report_command():
    input_choice = click.prompt(
        "Do you know the report ID, or would you like to search by student ID or list all reports? (id/student/list)")

    if input_choice.lower() == "id":
        report_id = click.prompt("Enter the report ID")
        report = Report.query.get(report_id)
        if report:
            review = click.prompt("Enter the new review", default=report.review)
            rating = click.prompt("Enter the new rating (1-5)", default=report.rating)
            result = update_report(report_id, review, rating)
            print(result)
        else:
            print("Report not found.")

    elif input_choice.lower() == "student":
        student_id = click.prompt("Enter the student ID to find their reports")
        student = get_student(student_id)
        if student:
            reports = get_student_reports(student.id)
            if not reports:
                print("No reports found for this student.")
                return

            print("Select a report to update:")
            for index, report in enumerate(reports, start=1):
                print(f"{index}\tID: {report.id}\tRating: {report.rating}\tReview: {report.review}")

            selected_index = click.prompt("Enter the number of the report you want to update: ")
            if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(reports):
                print("Invalid selection. Please try again.")
            else:
                selected_report = reports[int(selected_index) - 1]
                review = click.prompt("Enter the new review", default=selected_report.review)
                rating = click.prompt("Enter the new rating (1-5)", default=selected_report.rating)
                result = update_report(selected_report.id, review, rating)
                print(result)
        else:
            print("Student not found.")

    elif input_choice.lower() == "list":
        reports = get_all_reports('asc')
        if not reports:
            print("No reports found.")
            return

        print("Select a report to update:")
        for index, report in enumerate(reports, start=1):
            student = report.student
            print(
                f"{index}\tID: {report.id}\tStudent: {student.firstname} {student.lastname}\tRating: {report.rating}\tReview: {report.review}")

        selected_index = click.prompt("Enter the number of the report you want to update: ")
        if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(reports):
            print("Invalid selection. Please try again.")
        else:
            selected_report = reports[int(selected_index) - 1]
            review = click.prompt("Enter the new report")
            rating = click.prompt("Enter the new rating (1-5)")
            result = update_report(selected_report.id, review, rating)
            print(result)
    else:
        print("Invalid input. Please enter 'id', 'student', or 'list'.")


@staff_cli.command("delete_report", help="Deletes an existing report")
def delete_report_command():
    input_choice = click.prompt(
        "Do you want to delete by report ID, student ID, or student name? (id/student_id/student_name)")

    if input_choice.lower() == "id":
        report_id = click.prompt("Enter the report ID")
        result = delete_report(report_id)
        print(result)

    elif input_choice.lower() == "student_id":
        student_id = click.prompt("Enter the student ID to find their reports")
        student = get_student(student_id)
        if student:
            reports = get_student_reports(student.id)
            if not reports:
                print("No reports found for this student.")
                return

            print("Select a report to delete:")
            for index, report in enumerate(reports, start=1):
                print(f"{index}\tID: {report.id}\tRating: {report.rating}\tReview: {report.review}")

            selected_index = click.prompt("Enter the number of the report you want to delete: ")
            if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(reports):
                print("Invalid selection. Please try again.")
            else:
                selected_report = reports[int(selected_index) - 1]
                result = delete_report(selected_report.id)
                print(result)
        else:
            print("Student not found.")

    elif input_choice.lower() == "student_name":
        firstname = click.prompt("Enter the first name of the student")
        lastname = click.prompt("Enter the last name of the student")
        student = get_student_by_name(firstname, lastname)
        if student:
            reports = get_student_reports(student.id)
            if not reports:
                print("No reports found for this student.")
                return

            print("Select a report to delete:")
            for index, report in enumerate(reports, start=1):
                print(f"{index}\tID: {report.id}\tRating: {report.rating}\tReview: {report.review}")

            selected_index = click.prompt("Enter the number of the report you want to delete: ")
            if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(reports):
                print("Invalid selection. Please try again.")
            else:
                selected_report = reports[int(selected_index) - 1]
                result = delete_report(selected_report.id)
                print(result)
        else:
            print("Student not found.")

    else:
        print("Invalid input. Please enter 'id', 'student_id', or 'student_name'.")


app.cli.add_command(staff_cli)

'''
Student Commands
'''
student_cli = AppGroup('student', help='Commands involving students')


@student_cli.command("create", help="Adds a new student")
@click.argument("student_id", default="816021379")
@click.argument("firstname", default="Richard")
@click.argument("lastname", default="Mohammed")
def create_student_command(student_id, firstname, lastname):
    result = create_student(student_id, firstname, lastname)
    if isinstance(result, Student):
        print("Successfully created student: ", result.firstname, result.lastname)
        return
    print(result)


@student_cli.command("list", help="Lists all students")
def list_students_command():
    students = get_all_students()
    if students:
        print("Listing all students")
        print("ID\tFirst Name\tLast Name")
        print("-" * 40)
        for student in students:
            print(f"{student.student_id}\t{student.firstname}\t{student.lastname}")
    else:
        print("No students found")


@student_cli.command("get_report_by_id", help="Returns all reports for a student by ID")
@click.argument("id", default="816013456")
def get_report_by_id_command(id):
    student = get_student_by_id(id)

    if student:
        reports = get_student_reports(student.id)
        if not reports:
            print("No reports found for this ID")
            return
        print(f"Reports for student: {student.firstname} {student.lastname} (ID: {student.student_id})")
        print("ID\tRating\tDate\tReview")
        print("-" * 40)
        for report in reports:
            print(f"{report.id}\t{report.rating}\t{report.date.strftime('%Y-%m-%d')}\t{report.review}")
    else:
        print(f"Student with ID {id} not found.")


@student_cli.command("update_student", help="Updates an existing student")
def update_student_command():
    input_choice = click.prompt("Do you know the name or ID of the student you're trying to modify? (name/id/none)")

    if input_choice.lower() == "name":
        firstname = click.prompt("Enter the first name of the student")
        lastname = click.prompt("Enter the last name of the student")
        student = get_student_by_name(firstname, lastname)
        if student:
            new_student_id = click.prompt("Enter the new student ID")
            result = update_student(student.student_id, firstname, lastname, new_student_id)
            print("Student updated successfully")
        else:
            print("Student not found.")

    elif input_choice.lower() == "id":
        student_id = click.prompt("Enter the student ID")
        student = get_student(student_id)
        if student:
            new_student_id = click.prompt("Enter the new student ID")
            result = update_student(student.student_id, student.firstname, student.lastname, new_student_id)
            print("Student updated successfully")
        else:
            print("Student not found.")

    elif input_choice.lower() == "none":
        students = get_all_students()
        if not students:
            print("No students found.")
            return
        print("Select a student to update:")
        for index, student in enumerate(students, start=1):
            print(f"{index}\t{student.firstname}\t{student.lastname}\t(ID: {student.student_id})")

        selected_index = click.prompt("Enter the number of the student you want to update: ")
        if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(students):
            print("Invalid selection. Please try again.")
        else:
            student = students[int(selected_index) - 1]
            new_student_id = click.prompt("Enter the new student ID")
            result = update_student(student.student_id, student.firstname, student.lastname, new_student_id)
            print("Student updated successfully")

    else:
        print("Invalid input. Please enter 'name', 'id', or 'none'.")


@student_cli.command("delete", help="Deletes an existing student")
def delete_student_command():
    students = get_all_students()
    if not students:
        print("No students found.")
        return

    print("Select a student to delete:")
    for index, student in enumerate(students, start=1):
        print(f"{index}\t{student.firstname}\t{student.lastname}\t(ID: {student.student_id})")

    selected_index = input("Enter the number of the student you want to delete: ")
    if not selected_index.isdigit() or int(selected_index) < 1 or int(selected_index) > len(students):
        print("Invalid selection. Please try again.")
        return

    selected_student = students[int(selected_index) - 1]
    confirm = input(
        f"Are you sure you want to delete {selected_student.firstname} {selected_student.lastname} (ID: {selected_student.student_id})? (y/n): ")

    if confirm.lower() == 'y':
        result = delete_student(selected_student.student_id)
        print(f"{result}")


@student_cli.command("list_reports", help="Lists all reports")
@click.argument("order", default='asc')
def list_reports_command(order):
    reports = get_all_reports(order)
    if not reports:
        print("No reports found.")
        return

    print(f"Listing reports (order: {order})")
    print("ID\tStudent Name\tRating\tDate\tReview\tStaff Name")
    print("-" * 40)
    for report in reports:
        student = report.student
        print(
            f"{report.id}\t{student.firstname} {student.lastname}\t{report.rating}\t{report.date.strftime('%Y-%m-%d')}\t{report.review}\t{get_staff_by_id(report.staff_id).username}")


@student_cli.command("search_by_id", help="Search for a student by ID")
@click.argument("student_id", default="816021379")
def search_student_by_id_command(student_id):
    student = get_student_by_id(student_id)
    if isinstance(student, Student):
        print("Student found:")
        print("ID\tFirst Name\tLast Name")
        print("-" * 40)
        print(f"{student.student_id}\t{student.firstname}\t{student.lastname}")
    else:
        print(f"No student found with ID: {student_id}")


@student_cli.command("search_by_name", help="Search for students by first name and last name")
@click.argument("firstname")
@click.argument("lastname")
def search_students_by_name_command(firstname, lastname):
    student = get_student_by_name(firstname, lastname)
    if isinstance(student, Student):
        print(f"{student.student_id}\t{student.firstname}\t{student.lastname}")
        if student.reports:
            print("ID\tRating\tDate\tReview\tStaff Name")
        for report in student.reports:
            print(
                f"{report.id}\t{report.rating}\t{report.date.strftime('%Y-%m-%d')}\t{report.review}\t{get_staff_by_id(report.staff_id).username}")
    else:
        print(f"No students found matching the name: {firstname} {lastname}")


app.cli.add_command(student_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


@test.command("all", help="Run all tests (unit and integration)")
def all_tests_command():
    sys.exit(pytest.main(["-k", "integration_tests or unit_tests"]))


@test.command("unit", help="Run unit tests")
def unit_tests_command():
    sys.exit(pytest.main(["-k", "unit_tests"]))


@test.command("int", help="Run integration tests")
def integration_tests_command():
    """Runs integration tests."""
    sys.exit(pytest.main(["-k", "integration_tests"]))


app.cli.add_command(test)
