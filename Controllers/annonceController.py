from Controllers.baseController import *

def get_all_annonces(Annonce, Localisation):
    try:
        res_data = []
        annonces = Annonce.query.all()
        for annonce in annonces:
            res_annonce = annonce.toJSON()
            localisation = Localisation.query.filter_by(annonce_id = annonce.id).first()
            res_annonce["wilaya"] = localisation.wilaya
            res_data.append(res_annonce)
        return sendResponse(
            data=res_data,
            message='All announcements'
        )
    except Exception as e:
        return sendErrorMessage(
            message=str(e)
        )


# Deposer une annonce
def depotAnnonce(db, request, Utilisateur, Contact, Annonce, Localisation, id):
    try:
        user = Utilisateur.query.get_or_404(id)
        user_contact = Contact.query.filter_by(utilisateur_id=id).first()
        if (user_contact == None):
            user_contact = Contact(
                nom=user.nom,
                prenom=user.prenom,
                email=user.email,
                telephone=user.telephone,
                utilisateur=user
            )
        new_annonce = Annonce(
            titre=request.json['titre'],
            categorie=request.json['categorie'],
            type=request.json['type'],
            surface=request.json['surface'],
            description=request.json['description'],
            prix=request.json['prix'],
            utilisateur_id=id,
            contact=user_contact,
            localisation=None
        )
        db.session.add(new_annonce)
        db.session.commit()
        new_localisation = Localisation(
            wilaya=request.json['wilaya'],
            commune=request.json['commune'],
            adresse=request.json['adresse'],
            annonce_id=new_annonce.id
        )
        new_annonce.localisation = new_localisation
        db.session.add(new_localisation)
        db.session.commit()
        return sendResponse(
            data=new_annonce.toJSON(),
            message='Announcement added successfully'
        )
    except Exception as e:
        return sendErrorMessage(
            message=str(e)
        )


# Rechercher des annonces
def rechercheAnnonce(request, Annonce):
    try:
        search_text = request.form['search']
        searched_terms = search_text.split(' ')
        annonces_list = []
        for annonce in Annonce.query.all():
            desc = getattr(annonce, 'description')
            title = getattr(annonce, 'titre')
            for term in searched_terms:
                if (term in desc or term in title):
                    annonces_list.append(annonce.toJSON())
        return sendResponse(
            data=[annonce.toJSON() for annonce in annonces_list],
            message='Liste des annonces'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


# Afficher les details d'une annonce
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


# Consultation des annonces deposees
def annoncesDeposees(id, Annonce):
    try:
        annonces = Annonce.query.filter_by(utilisateur_id=id)
        return sendResponse(
            data=[annonce.toJSON() for annonce in annonces],
            message='Liste des annonces associées'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


# Supprimer annonce
def supprimerAnnonce(db, user_id, annonce_id, Annonce):
    try:
        if (annonceDUtilisateur(user_id, annonce_id, Annonce)):
            annonce = Annonce.query.get_or_404(id)
            db.session.delete(annonce)
            db.session.commit()
            return sendResponse(
                data=[],
                message='Annonce suprimeé'
            )
        else:
            return sendErrorMessage(
                message='Something went wrong'
            )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


# Verifier si l'annonce appartient a user_id
def annonceDUtilisateur(user_id, annonce_id, Annonce):
    annonce = Annonce.query.get_or_404(annonce_id)
    return (annonce.utilisateur_id == user_id)
