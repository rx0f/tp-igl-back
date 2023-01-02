from app import session


#Deposer une annonce
def depotAnnonce(db, request, Utilisateur, Contact, Annonce):
    try:
        id = getattr(session, 'utilisateur_id')
    except:
        id = 1
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
    return {
        'data': new_annonce.toJSON(),
        'message': 'Announcement added successfully'
    }
    


#Rechercher des annonces
def rechercheAnnonce(request, Annonce):
    search_text = request.form['search']
    searched_terms = search_text.split(' ')
    annonces_list = []
    for annonce in Annonce.query.all():
        desc = getattr(annonce, 'description')
        title = getattr(annonce, 'titre')
        for term in searched_terms:
            if(term in desc or term in title):
                annonces_list.append(annonce)
    return annonces_list
    
    
    
#Afficher les details d'une annonce
def detailsAnnonce(id, Annonce):
    annonce = Annonce.query.get_or_404(id)
    return annonce.toJSON()


#Consultation des annonces deposees
def annoncesDeposees(id, Annonce):
    annonces = Annonce.query.filter_by(utilisateur_id=id)
    return [annonce.toJSON() for annonce in annonces]


#Supprimer annonce
def supprimerAnnonce(db, id, Annonce):
    try:
        annonce = Annonce.query.get_or_404(id)
        db.session.delete(annonce)
        db.session.commit()
        return {
            'result': True,
            'message': 'Announcemet deleted'
        }
    except:
        return {
            'result': False,
            'message': 'Something went wrong'
        }
        
#Verifier si l'annonce appartient a user_id
def annonceDUtilisateur(user_id, annonce_id, Annonce):
    annonce = Annonce.query.get_or_404(annonce_id)
    return (annonce.id == user_id)