# FastAPI OAuth2 Client 

### WSO2 Identity Server compatible

This project is a proof of concept how to implement `Authorization Code` grant type with WSO2 Identity Server. 
With minor adjustments, or even without changes, it can talk with other OAuth2 servers as well.

As a result, it'll get JWT token from WSO2 Identity Server, then validate it by invoking public JWKS endpoint. The JSON Web Key Set (JWKS) is a set of keys containing the public keys used to verify any JSON Web Token (JWT) issued by the Authorization Server and signed using the RS256 signing algorithm.

### How to use it
- Clone the repo
- run `cp .env.example .env`
- edit `.env` and fill up your own parameters
- run `pip3 install -r requirements.txt` 
- run `uvicorn main:app --port 3000  --reload`
- open http://localhost:3000/login in web browser
- you should be redirected to the login page
- after a successful login, you should get back the token response in JSON format, e.g.:
```
{
    "sub": "dusandevic@gmail.com",
    "aut": "APPLICATION",
    "iss": "https://identity.diplomacy.edu/oauth2/token",
    "given_name": "Dusan",
    "client_id": "xxx",
    "aud": "xxx",
    "nbf": 1679487318,
    "azp": "xxx",
    "scope": "profile",
    "exp": 1679490918,
    "iat": 1679487318,
    "family_name": "Devic",
    "jti": "d8760edc-8069-430c-a732-6c2b77716a29",
    "username": "dusandevic@gmail.com"
}
```
Returned token might be a bit different as it depends on the WSO2 Identity Server Service Provider configuration. 
One should pre-configure it in WSO2 Identity Server in order to get configuration parameters (client id, secret, callback url etc). 


### Author
- Dusan Devic 
- dusandevic@gmail.com