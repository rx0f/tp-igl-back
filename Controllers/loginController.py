from app import session
from functools import wraps
from Controllers.baseController import *
from flask import request

# Login Function


def loginFunction(db, request, Utilisateur):
    try:
        in_email = request.json['email']
        user = Utilisateur.query.filter_by(email=in_email).first()
        if (user == None):
            new_user = Utilisateur(
                nom='',
                prenom='',
                email=in_email,
                telephone='',
                role_id=1,
                confirmed_data=0

            )
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user.id
            session.permanent = True
            return sendResponse(
                data=new_user.toJSON(),
                message='Account created successfully'
            )
        else:
            session['user'] = user.id
            session.permanent = True
            return sendResponse(
                data=user.toJSON(),
                message='Logged in successfully'
            )
    except Exception as e:
        return sendErrorMessage(
            message=str(e)
        )


# Logout function
def user_logout():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return sendResponse(
            data=None,
            message='User logged out successfully'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if (request.headers['Authorization']):
                return f(*args, **kwargs)
        except Exception as e:
            return sendErrorMessage(
                message=str(e)
            )
    return decorated_function
