from authlib.integrations.flask_client import OAuth
from app import app as new_app


# oAuth Setup
oauth = OAuth(new_app)
google = oauth.register(
    name='google',
    client_id="870779871721-7t2n4jbls2sft5349bq9iq0lddqp8ouo.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'email profile'},
    server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration'
)