from app import session

#Login Function
def login(request, Utilisateur):
    in_email=request.form['email']
    utilisateur = Utilisateur.query.filter_by(email=in_email).first()
    if(utilisateur==None):
        return {
            'result': False,
            'message': 'No account with given email'
        }
    current_user = getattr(utilisateur, 'id')
    setattr(session, 'utilisateur_id', current_user)
    return {
            'result': True,
            'data': utilisateur.toJSON(),
            'message': 'Login successful'
        }
            
            

#Sign in Function
def signin(db, request, Utilisateur):
    in_email=request.form['email']
    utilisateur = Utilisateur.query.filter_by(email=in_email).first()
    if(utilisateur==None):
        in_tel=request.form['tel']
        in_nom=request.form['nom']
        in_prenom=request.form['prenom'] 
        new_user = Utilisateur(
            nom=in_nom,
            prenom=in_prenom,
            email=in_email,
            telephone=in_tel,
            role_id = 1
        )
        db.session.add(new_user)
        db.session.commit()
        return {
            'result': True,
            'message': 'Signed in successfully'
        }
    else:
        return {
            'result': False,
            'message': 'Account found with given email'
        }