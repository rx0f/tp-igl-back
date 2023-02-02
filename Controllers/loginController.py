from app import session
from flask import Flask
from functools import wraps
from Controllers.baseController import *

#Login Function
def loginFunction(db, request, Utilisateur):
    try:
        in_email = request.form['email']
        user = Utilisateur.query.filter_by(email=in_email).first()
        if(user==None):
            new_user = Utilisateur(
                nom='',
                prenom='',
                email = in_email,
                telephone = '',
                role_id = 1,
                confirmed_data = 0
                
            )
            db.session.add(new_user)
            db.session.commit()
            return sendResponse(
                data = new_user,
                message = 'Account created successfully'
            )
        else:
            session['user'] = user.id
            session.permanent = True
            return sendResponse(
                data=user.toJSON(),
                message='Logged in successfully'
            )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )     

        
        
#Logout function
def user_logout():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return sendResponse (
            data=None,
            message='User logged out successfully'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )



        
#Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
           if(session['user']):
               return f(*args, **kwargs)
        except Exception as e:
            return sendErrorMessage(
                message='You are not logged in'
            )
    return decorated_function