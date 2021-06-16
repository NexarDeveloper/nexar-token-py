"""Main entry point to the service."""
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import MissingTokenError
from requests_oauthlib import OAuth2Session


PROD_TOKEN_URL = "https://identity.nexar.com/connect/token"


def get_token(client_id, client_secret):
    """Return the nexar token from the client_id and client_secret provided."""
    if not client_id or not client_secret:
        raise Exception("client_id and/or client_secret are empty")

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = {}
    try:
        token = oauth.fetch_token(
            token_url=PROD_TOKEN_URL,
            client_id=client_id,
            client_secret=client_secret,
            include_client_id=True
        )
    except MissingTokenError:
        raise

    return token
