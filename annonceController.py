from app import session
from baseController import *


#Deposer une annonce
def depotAnnonce(db, request, Utilisateur, Contact, Annonce, id):
    try:
        user = Utilisateur.query.get_or_404(id)
        user_contact = Contact.query.filter_by(utilisateur_id = id).first()
        if (user_contact==None):
            user_contact = Contact (
                nom = user.nom,
                prenom = user.prenom,
                adresse='TBD',
                email = user.email,
                telephone = user.telephone,
                utilisateur = user
            )
        new_annonce = Annonce(
            titre = request.form['titre'],
            categorie = request.form['categorie'],
            type = request.form['type'],
            surface = request.form['surface'],
            description = request.form['description'],
            prix = request.form['prix'],
            utilisateur_id = id,
            contact = user_contact,
            localisation = None
        )
        db.session.add(new_annonce)
        db.session.commit()
        return sendResponse(
            data=new_annonce.toJSON(),
            message='Announcement added successfully'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )
    


#Rechercher des annonces
def rechercheAnnonce(request, Annonce):
    try:
        search_text = request.form['search']
        searched_terms = search_text.split(' ')
        annonces_list = []
        for annonce in Annonce.query.all():
            desc = getattr(annonce, 'description')
            title = getattr(annonce, 'titre')
            for term in searched_terms:
                if(term in desc or term in title):
                    annonces_list.append(annonce.toJSON())
        return sendResponse(
            data=annonces_list,
            message='Liste des annonces'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )
    
    
    
#Afficher les details d'une annonce
def detailsAnnonce(id, Annonce):
    try:
        annonce = Annonce.query.get_or_404(id)
        return sendResponse(
            data=annonce.toJSON(),
            message='Annonce detailees'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


#Consultation des annonces deposees
def annoncesDeposees(id, Annonce):
    try:
        annonces = Annonce.query.filter_by(utilisateur_id=id)
        return sendResponse(
            data= [annonce.toJSON() for annonce in annonces],
            message='Liste des annonces associées'
        ) 
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


#Supprimer annonce
def supprimerAnnonce(db, id, Annonce):
    try:
        annonce = Annonce.query.get_or_404(id)
        db.session.delete(annonce)
        db.session.commit()
        return sendResponse(
            data=[],
            message='Annonce suprimeé'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )
        

#Verifier si l'annonce appartient a user_id
def annonceDUtilisateur(user_id, annonce_id, Annonce):
    annonce = Annonce.query.get_or_404(annonce_id)
    return (annonce.id == user_id)