from flask import Flask, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

db = SQLAlchemy()

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tp.db'

db.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from Models.models import Utilisateur, Annonce, Contact, Message
from Controllers.loginController import *
from Controllers.annonceController import *
from Controllers.messagingController import *
from authInit import oauth

migrate = Migrate(app, db)


@app.route("/")
def index():
    return 'Hello, World!'


@app.route('/test')
def test():
    data = session['profile']
    email = dict(session)['profile']['email']
    return f'Hello, you are logge in as {email}!  {data}'


@app.route('/login')
def login():
    return oAuthLinkGenerate(oauth, url_for, 'login')


@app.route('/authorize_login')
def authorize_login():
    resp = authorizeLogin(oauth, Utilisateur)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route('/sign_in')
def signin_page():
    return oAuthLinkGenerate(oauth, url_for, 'sign_in')


@app.route('/authorize_sign_in')
def authorize_sign_in():
    resp = authorizeSignIn(oauth, Utilisateur, db)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.post('/logout')
@login_required
def logout():
    return user_logout()



@app.post('/users')
@login_required
def get_users():
    users = Utilisateur.query.all()
    return [user.toJSON() for user in users]



@app.post('/user/<int:id>')
@login_required
def user_account(id):
    user = Utilisateur.query.get(id)
    if(user):
        return user.toJSON()
    else:
        return {
            'message': 'user not found'
        }


@app.post('/user/<int:id>/depot_annonce')
def depot_annonce(id):
    return depotAnnonce(db, request, Utilisateur, Contact, Annonce, id)
    

@app.post('/user/<int:id>/recherche_annonce')
def recherche_annonce(id):
    annonces = rechercheAnnonce(request, Annonce)
    return[annonce.toJSON() for annonce in annonces]



@app.post('/annonces')
def annonce_list():
    annonces = Annonce.query.all()
    return [annonce.toJSON() for annonce in annonces]


@app.post('/annonces/<int:id>')
def details_annonce(id):
    return detailsAnnonce(id, Annonce)

@app.post('/user/<int:id>/annonces')
def annonces_deposees(id):
    return annoncesDeposees(id, Annonce)

@app.post('/user/<int:user_id>/annonces/<int:annonce_id>/delete/')
def supprimer_annonce(user_id, annonce_id):
    return supprimerAnnonce(db, user_id, annonce_id, Annonce)


@app.post('/user/<int:id>/messages')
def messages_recus(id):
    return viewMessages(db, id, Message)


@app.post('/user/<int:user_id>/annonces/<int:annonce_id>/message')
def envoyer_offre(user_id, annonce_id):
    return sendMessage(db, request, user_id, annonce_id, Message, Annonce)


if __name__=='__main__':
    app.run(Debug=True)