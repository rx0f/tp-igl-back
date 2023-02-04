from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, support_credentials=True)

app.config["CORS_EXPOSE_HEADERS"] = "*"

db = SQLAlchemy()

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tp.db'

db.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from Models.models import *
from Controllers.loginController import *
from Controllers.annonceController import *
from Controllers.messagingController import *
from Controllers.photoController import *
from Controllers.userController import *


@app.after_request
def after_request(response):
  response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


@app.route("/")
def index():
    return 'Hello, World!'


@app.route('/test')
def test():
    data = session['user']
    id = dict(session)['user']
    return f'Hello, you are logge in as user#{id}!  {data}'


@app.post('/login')
@cross_origin(supports_credentials=True)
def login():
    return loginFunction(db, request, Utilisateur)



@app.post('/logout')
@login_required
def logout():
    return user_logout()



@app.get('/users')
def get_users():
    return get_all_users(Utilisateur)



@app.route('/user/<int:id>', methods=["GET", "PUT"])
@login_required
def user_account(id):
    if request.method == "GET":
        return get_user(Utilisateur, id)
    if request.method == "PUT":
        return edit_user(db, Utilisateur, id)


@app.post('/user/<int:id>/depot_annonce')
def depot_annonce(id):
    return depotAnnonce(db, request, Utilisateur, Contact, Annonce, Localisation, id)
    


@app.post('/user/<int:id>/recherche_annonce')
def recherche_annonce(id):
    return rechercheAnnonce(request, Annonce)



@app.get('/annonces')
def annonce_list():
    return get_all_annonces(Annonce, Localisation)


@app.get('/annonces/<int:id>')
def details_annonce(id):
    return detailsAnnonce(id, Annonce, Contact)


@app.get('/user/<int:id>/annonces')
def annonces_deposees(id):
    return annoncesDeposees(id, Annonce, Localisation)


@app.delete('/user/<int:user_id>/annonces/<int:annonce_id>')
def supprimer_annonce(user_id, annonce_id):
    return supprimerAnnonce(db, user_id, annonce_id, Annonce)


@app.post('/user/<int:id>/messages')
def messages_recus(id):
    return viewMessages(db, id, Message)


@app.post('/user/<int:user_id>/annonces/<int:annonce_id>/message')
def envoyer_offre(user_id, annonce_id):
    return sendMessage(db, request, user_id, annonce_id, Message, Annonce)


@app.route('/annonces/<int:annonce_id>/add_photo')
def imageAdd(annonce_id):
    return f"<form action = '/upload_image' method = 'post' enctype='multipart/form-data'><input type='file' name='file' /><input type='hidden' name='annonce_id' value={annonce_id}><input type = 'submit' value='Upload'></form>"


@app.post('/upload_photo')
def uploadImage():
    return photoAdded(db, request.form['annonce_id'], Photo)


@app.post('/photos/<int:id>/delete_photo')
def delPhoto(id):
    return deletePhoto(db, id, Annonce, Photo)


if __name__=='__main__':
    app.run(Debug=True)