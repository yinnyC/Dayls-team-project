"""Import packages and modules."""

import os
from flask import Blueprint, request, render_template, redirect, url_for, session, flash

# Import app and db from events_app package so that we can run app
from events_app import app, auth, firebase
from events_app.main.utils import getUserID, getRecruiterProfile

recruiter = Blueprint("recruiter", __name__)
main = Blueprint("main", __name__)


@recruiter.route('/recruiter/main')
def recruiter_main():
    """
    Return template for recruiter profile.
    """
    if session['user']:
        user = getUserID()  # To access to the currenr user's uid
        data = getRecruiterProfile(user)
        return render_template('Recruiters/profile_info.html', **data)
    else:
        print("please login first")
        return redirect(url_for("main.homepage"))


@recruiter.route('/recruiter/create_profile', methods=['GET', 'POST'])
def create_recruiter_profile():
    if session['user']:  # Check if user has logged in yet
        if request.method == "GET":
            return render_template('Recruiters/create_profile.html')
        elif request.method == "POST":
            data = {
                "name": request.form.get("name"),
                "bio": request.form.get("bio"),
                "company": request.form.get("company"),
                "title": request.form.get("title"),
                "talent": ",".join(request.form.getlist('talent')),
            }
            user = getUserID()
            firebase.database().child("recruiter_profile").child(user).update(
                data)
            print('data inserted')
            return redirect(url_for("recruiter.recruiter_main"))

    else:
        print("You need to log in first")
        return redirect(url_for("main.homepage"))


@recruiter.route('/recruiter/update_profile', methods=['GET', 'POST'])
def update_recruiter_profile():
    """ The function can update data for the recruiter profile """
    if session['user']:
        if request.method == "GET":
            user = getUserID()  # To access to the currenr user's uid
            data = getRecruiterProfile(user)
            return render_template('Recruiters/update_profile.html', **data)
        elif request.method == "POST":
            data = {
                "name": request.form.get("name"),
                "bio": request.form.get("bio"),
                "company": request.form.get("company"),
                "title": request.form.get("title"),
                "talent": request.form.get("talent"),
            }
            user = getUserID()
            firebase.database().child("recruiter_profile").child(user).update(
                data)
            print('data updated!')
            return redirect(url_for("recruiter.recruiter_main"))
    else:
        print("You have to be logged in first!")
        return redirect(url_for("main.homepage"))

@recruiter.route('/recruiter/show_students')
def show_students():
    """
    Return template for student profile.
    """
    if session['user']:
        student_profile = firebase.database().child('student_profile').get()
        student_profile = [student.val() for student in student_profile.each()]
        return render_template('Recruiters/student_grid.html', student_profile= student_profile)
    else:
        print("please login first")
        return redirect(url_for("main.homepage"))