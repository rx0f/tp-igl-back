from app import db


class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), unique=False, nullable=False)
    prenom = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telephone = db.Column(db.String, unique=False, nullable=False)
    confirmed_data = db.Column(db.Integer, unique=False, nullable=False)
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
    
    def toJSON(self):
        return {
            'id': self.id,
            'url': self.url,
            'annonce_id': self.annonce_id
        }
    
    
    


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