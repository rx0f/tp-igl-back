from Controllers.baseController import *
from flask import request


def get_all_users(Utilisateur):
    try:
        users = Utilisateur.query.all()
        return sendResponse(
            data=[user.toJSON() for user in users],
            message='Users list'
        )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )


def edit_user(db, Utilisateur, id):
    try:
        user = Utilisateur.query.get(id)
        user.nom = request.json["nom"]
        user.prenom = request.json["prenom"]
        user.telephone = request.json["telephone"]
        db.session.commit()
        return sendResponse(
            data=user.toJSON(),
            message="User data updated"
        )
    except Exception as e:
        return sendErrorMessage(
            message=str(e)
        )


def get_user(Utilisateur, id):
    try:
        user = Utilisateur.query.get(id)
        if (user):
            return sendResponse(
                data=user.toJSON(),
                message='User data retrieved'
            )
        else:
            return sendErrorMessage(
                message='user not found'
            )
    except Exception as e:
        return sendErrorMessage(
            message=str(e)
        )
