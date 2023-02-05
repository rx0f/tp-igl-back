from Controllers.baseController import *

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


def sendMessage(db, request, recipient_id, Message):
    try:
        new_message = Message(
            content = request.json['content'],
            sender_id = request.json['sender_id'],
            recipient_id = recipient_id
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