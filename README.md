# nexar-token-py
Getting Nexar tokens for Python.


## Installing the python packages:
Using the virtual environment manager of your choice (venv, conda, etc.), install the python packages:

`pip install -r requirements.txt`


## Importing as an external module
This repository can be imported as a submodule or subtree from another repository.

After adding the submodule/subtree it can be implemented as follows:

`from nexar_module.nexar_token import get_token`

## Obtaining Nexar token
The following command will obtain and copy the Nexar token to the clipboard.

`python print_token.py <CLIENT_ID> <CLIENT_SECRET>`

## Obtaining Nexar token with login
The following command will obtain and copy the Nexar token with login to the clipboard.

`python print_token_with_login.py <CLIENT_ID> <CLIENT_SECRET> <SCOPE_1> <SCOPE2> ...`

where scopes include:
- user.access
- design.domain
- supply.domain

If no scopes are given then these three scopes will be used by default


e.g. `python print_token_with_login.py <CLIENT_ID> <CLIENT_SECRET>`

The login will open a browser tab asking for the login credentials and then display a page
indicating whether the given credentials are vaild.  This tab may then be closed while the
token is generated and copied to the clipboard.


## Sample request for extracting GraphQL part data
With the token copied to the clipboard, the sample_request can be run to query the Nexar API
`python sample_request.py <MPN>`

Please note that any changes to the clipboard will require the token to be re-copied before
running the sample request.


## Extra info
Some information and examples of the package used:
https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow
