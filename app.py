from flask import Flask, redirect, url_for, render_template, request, make_response, session
from flask_sqlalchemy import session, SQLAlchemy
from flask_migrate import Migrate, migrate
from loginController import *
from annonceController import *
from messagingController import *

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tp.db'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if(request.method=='GET'):
        return render_template('login.html')
    else:
        response = login(request, Utilisateur)
        if(response['result']):
            return response['data']
        else:
            return response['message']



@app.route('/sign_in', methods=['GET', 'POST'])
def signin_page():
    if(request.method=='GET'):
        return render_template('signin.html')
    else:
        response = signin(db, request, Utilisateur)
        if(response['result']):
            resp = make_response(render_template('index.html'))
            return resp
        else:
            return render_template('signin.html', errors=response['message'])



@app.post('/users')
def get_users():
    users = Utilisateur.query.all()
    return [user.toJSON() for user in users]



@app.post('/user/<int:id>')
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
def messages_reçus(id):
    return viewMessages(db, id, Message)


@app.post('/user/<int:user_id>/annonces/<int:annonce_id>/message')
def envoyer_offre(user_id, annonce_id):
    return sendMessage(db, request, user_id, annonce_id, Message, Annonce)


if __name__=='__main__':
    app.run(Debug=True)
    

#------------------------------- Models' Definitions--------------------------------#

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), unique=False, nullable=False)
    prenom = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telephone = db.Column(db.String, unique=False, nullable=False)
    role_id = db.Column(db.Integer, unique=False, nullable=False)
    contact_id = db.relationship('Contact', uselist=False, backref='utilisateur')
    list_deposees = db.relationship('Annonce', backref='utilisateur')
    
    
    
    def __repr__(self):
        return f'User#{self.id}. Name : {self.first_name} {self.last_name}'
    
    def toJSON(self):
        return {
            'id': self.id,
            'nom' : self.nom,
            'prenom' : self.prenom,
            'email' : self.email,
            'telephone' : self.telephone,
            'role_id' : self.role_id
        }
    

class Annonce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String, unique=False, nullable=False)
    categorie = db.Column(db.String(20), unique=False, nullable=False)
    type = db.Column(db.String(20), unique=False, nullable=False)
    surface = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    prix = db.Column(db.Float, nullable=False)
    list_photos = db.relationship('Photo', backref='annonce')
    localisation = db.relationship('Localisation', uselist=False, backref='annonce')
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    
    def __repr__(self):
        return f'Annonce# {self.id}'
    
    def toJSON(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'categorie': self.categorie,
            'type': self.type,
            'surface': self.surface,
            'description': self.description,
            'prix': self.prix,
            'contact_id': self.contact_id,
            'utilisateur_id': self.utilisateur_id
        }
    
    
    
    
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    annonce_id = db.Column(db.Integer, db.ForeignKey('annonce.id'), nullable=False)
    
    def __repr__(self):
        return f'Photo# {self.id}'
    

class Localisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wilaya = db.Column(db.String, nullable=False)
    commune = db.Column(db.String, nullable=False)
    adresse = db.Column(db.String, nullable=False)
    annonce_id = db.Column(db.Integer, db.ForeignKey('annonce.id'))
    
    def __repr__(self):
        return f'{self.wilaya} - {self.commune} - {self.adresse}'
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    prenom = db.Column(db.String, nullable=False)
    adresse = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    telephone = db.Column(db.String, nullable=False)
    annonces = db.relationship('Annonce', backref='contact')
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    
    def __repr__(self):
        return f'Contact de {self.nom} {self.prenom}'
    
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    
    sender = db.relationship('Utilisateur', foreign_keys=[sender_id])
    recipient = db.relationship('Utilisateur', foreign_keys=[recipient_id])
    
    def __repr__(self):
        return f'Message de {self.sender_id} pour {self.recipient_id}'
    
    def toJSON(self):
        return {
            'id': self.id,
            'content': self.content,
            'sender_id': self.sender_id,
            'recipient_id' : self.recipient_id
        }