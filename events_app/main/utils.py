"""Helper functions for app."""
from flask import session
from events_app import app, auth, firebase


##########################################
#         Auth Helper Functions          #
##########################################
def getUserID():
    token = session['user']  # To access to the currenr user's uid
    try:  # To make sure the token is valid
        user = auth.get_account_info(token)['users'][0]['localId']
        return user
    except:  # If the token is invalid, return None and redirect user to login again
        return None


def loginUser(email, password):
    sign_user = auth.sign_in_with_email_and_password(email, password)
    sign_user = auth.refresh(sign_user['refreshToken'])
    session['user'] = sign_user['idToken']


def getUserRole():
    user = getUserID()
    role = firebase.database().child("Role").child(user).get()
    role_data = role.val()
    return role_data['role']


##########################################
#    Student Profile Helper Functions    #
##########################################


def getStudentProfile(userID):
    collection = "student_profile"
    user_profile = firebase.database().child(collection).child(userID).get()
    user_profile_data = user_profile.val()
    data = {
        "name": user_profile_data['name'],
        "bio": user_profile_data['bio'],
        "school": user_profile_data['school'],
        "degree": user_profile_data['degree'],
        "graduationDate": user_profile_data['graduationDate'],
    }
    return data


##########################################
#   Recruiter Profile Helper Functions   #
##########################################


def getRecruiterProfile(userID):
    collection = "recruiter_profile"
    user_profile = firebase.database().child(collection).child(userID).get()
    user_profile_data = user_profile.val()
    data = {
        "name": user_profile_data['name'],
        "bio": user_profile_data['bio'],
        "company": user_profile_data['company'],
        "title": user_profile_data['title'],
        "talent": user_profile_data['talent'],
    }
    return data