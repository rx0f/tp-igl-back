from Controllers.baseController import *
from flask import request
import os

def photoAdded(db, annonce__id, Photo):
    try:
        image = request.files['file']
        image.save(os.path.join('uploads', image.filename))
        new_image = Photo (
            url = '/uploads'+image.filename,
            annonce_id = annonce__id
        )
        db.session.add(new_image)
        db.session.commit()
        return sendResponse(
            data = new_image.toJSON(),
            message = f'image added successfully at {new_image.url}'
        )
    except:
        return sendErrorMessage(
            message = 'Something went wrong'
        )
        
def deletePhoto(id, Annonce, Photo):
    try:
        photo = Photo.query.get_or_404(id)
        owner_id = Annonce.query.get_or_404(photo.annonce_id).toJSON().utilisateur_id
        if(photo.id == 4):
            pass
    except:
        pass