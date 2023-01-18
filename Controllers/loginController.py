from app import session
from flask import Flask
from functools import wraps
from Controllers.baseController import *


def oAuthLinkGenerate(oauth, url_for, url):
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize'+'_'+url, _external=True)
    resp = google.authorize_redirect(redirect_uri)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp




#Login Function
def login(in_email, Utilisateur, user_info):
    try:
        user = Utilisateur.query.filter_by(email=in_email).first()
        if(user==None):
            return sendErrorMessage(
                message='No user found for given email'
            )
        else:
            session['profile'] = user_info
            session.permanent = True
            return sendResponse(
                data=user.toJSON(),
                message='Logged in successfully'
            )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )     
            

#Sign in Function
def signin(db, in_email, Utilisateur, user_info):
    try:
        new_user = Utilisateur.query.filter_by(email=in_email).first()
        if(new_user==None):
            in_tel=''
            in_nom=''
            in_prenom=''
            new_user = Utilisateur(
                nom=in_nom,
                prenom=in_prenom,
                email=in_email,
                telephone=in_tel,
                role_id = 1
            )
            db.session.add(new_user)
            db.session.commit()
            session['profile'] = user_info
            session.permanent = True
            return sendResponse(
                data=new_user.toJSON(),
                message='Signed in successfully'
            )
        else:
            return sendErrorMessage(
                message='User found with given email'
            )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )
        
        
        
def authorizeSignIn(oauth, Utilisateur, db):
    try:
        google = oauth.create_client('google')  # create the google oauth client
        token = google.authorize_access_token()  # Access token from google (needed to get user info)
        resp = google.get('userinfo', token=token)  # userinfo contains stuff u specificed in the scrope
        user_info = resp.json()
        user_email = user_info['email']
        return signin(db, user_email, Utilisateur, user_info)
    except Exception as e:
        return sendErrorMessage(
            message=str(e)
        )
        

def authorizeLogin(oauth, Utilisateur):
    try:
        google = oauth.create_client('google')  # create the google oauth client
        token = google.authorize_access_token()  # Access token from google (needed to get user info)
        resp = google.get('userinfo', token=token)  # userinfo contains stuff u specificed in the scrope
        user_info = resp.json()
        user_email = user_info['email']
        return login(user_email, Utilisateur, user_info)
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
           if(session['profile']):
               return f(*args, **kwargs)
        except Exception as e:
            return sendErrorMessage(
                message='You are not logged in'
            )
    return decorated_function