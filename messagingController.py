from baseController import *

def viewMessages(db, id, Message):
    try:
        messages = Message.query.filter_by(recipient_id=id)
        return sendResponse(
            data = [message.toJSON() for message in messages],
            message = 'Messages reçus'
        )
    except Exception as e:
        return sendErrorMessage(
            message = str(e)
        )


def sendMessage(db, request, user_id, annonce_id, Message, Annonce):
    try:
        recipient = Annonce.query.get(annonce_id)
        new_recipient_id = recipient.id
        new_message = Message (
            content = request.form['content'],
            sender_id = user_id,
            recipient_id = new_recipient_id
        )
        db.session.add(new_message)
        db.session.commit()
        return sendResponse(
            data = new_message.toJSON(),
            message = 'Message envoye'
        )
    except Exception as e:
        return sendErrorMessage(
            message = str(e)
        )