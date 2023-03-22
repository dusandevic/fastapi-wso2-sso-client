import string
from fastapi import FastAPI, Request
from authlib.integrations.requests_client import OAuth2Session
from fastapi.responses import RedirectResponse
import uvicorn
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

token_endpoint = os.getenv('TOKEN_ENDPOINT')
authorization_endpoint = os.getenv('AUTHORIZATION_ENDPOINT')
redirect_uri = os.getenv('REDIRECT_URI')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
jwks_endpoint = os.getenv('JWKS_ENDPOINT')
scope = 'openid profile'

session = OAuth2Session(client_id, client_secret, None, None, scope, None, redirect_uri)


@app.get("/login")
def login():
    uri, state = session.create_authorization_url(url=authorization_endpoint)
    response = RedirectResponse(url=uri, status_code=302)
    return response


@app.get("/oauth2/callback")
def oauth2Callback(request: Request):
    try:
        queryParams = request.query_params
        token_response = session.fetch_token(url=token_endpoint, grant_type='authorization_code', code=queryParams["code"])
        jwtToken = token_response["id_token"]
        return validateToken(jwtToken)
    except Exception as e:
        return {"message": str(e), "error": True}


def validateToken(jwtToken: string):
    try:
        # get public key from jwks uri
        jwks_client = PyJWKClient(jwks_endpoint)
        signing_key = jwks_client.get_signing_key_from_jwt(jwtToken)

        # get the algorithm type from the request header
        header = jwt.get_unverified_header(jwtToken)
        algorithm = header["alg"]

        # finally try to decode the token
        data = jwt.decode(
            jwt=jwtToken,
            key=signing_key.key,
            audience=client_id,
            algorithms=algorithm,
            options={"verify_exp": True},
        )

        return data
    except Exception as e:
        return {"message": str(e), "error": True}


if __name__ == '__main__':
    uvicorn.run(app, port=3000, host='0.0.0.0')
