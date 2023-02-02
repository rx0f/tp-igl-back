from Controllers.baseController import *

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


def get_user(Utilisateur, id):
    try:
        user = Utilisateur.query.get(id)
        if(user):
            return sendResponse(
                data=user.toJSON(),
                message='User data retrieved'
            )
        else:
            return sendErrorMessage(
                message='user not found'
            )
    except:
        return sendErrorMessage(
            message='Something went wrong'
        )