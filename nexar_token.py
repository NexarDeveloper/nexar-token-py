"""Main entry point to the service."""
import base64
import hashlib
import os
import re
import webbrowser
from multiprocessing import Process
from urllib.parse import parse_qs, urlparse

import requests
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import MissingTokenError
from requests_oauthlib import OAuth2Session

from local_service import main

PROD_TOKEN_URL = "https://identity.nexar.com/connect/token"
REDIRECT_URI = "http://localhost:3000/login"
AUTHORITY_URL = "https://identity.nexar.com/connect/authorize"


def get_token(client_id, client_secret):
    """Return the Nexar token from the client_id and client_secret provided."""
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
            include_client_id=True,
        )
    except MissingTokenError:
        raise

    return token


def get_token_with_login(client_id, client_secret, scope):
    """Open the Nexar authorization url from the client_id and scope provided."""
    if not client_id or not client_secret:
        raise Exception("client_id and/or client_secret are empty")
    if not scope:
        raise Exception("scope is empty")

    token = {}
    scope_list = ["openid", "profile", "email", "user.details"] + scope

    # Start the local service
    server = Process(target=main)
    server.daemon = True
    server.start()

    # PCKE code verifier and challenge
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    try:
        # Request login page
        oauth = OAuth2Session(client_id, redirect_uri=REDIRECT_URI, scope=scope_list)
        authorization_url, _ = oauth.authorization_url(
            url=AUTHORITY_URL,
            code_challenge=code_challenge,
            code_challenge_method="S256",
        )
        authorization_url = authorization_url.replace("+", "%20")

        # Obtain redirect response
        webbrowser.open_new(authorization_url)
        redirect_response = input(
            "\nPlease authorize access and enter the redirect URL: "
        ).strip()

        # Terminate the local service because no longer needed
        server.terminate()

        redirect_params = parse_qs(urlparse(redirect_response).query)
        auth_code = redirect_params["code"][0]
        token = requests.post(
            url=PROD_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_response,
                "code": auth_code,
                "code_verifier": code_verifier,
            },
            allow_redirects=False,
        ).json()
    except Exception:
        raise

    return token
