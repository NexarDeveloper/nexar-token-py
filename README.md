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
The following command will obtain and print the Nexar token.

`python print_token.py <CLIENT_ID> <CLIENT_SECRET> <SCOPE_1> <SCOPE2> ...`

where scopes include:
- user.access
- design.domain
- supply.domain

If any scopes other than supply.domain are requested the login will open a browser tab 
asking for the user credentials and then display a page indicating whether the given
credentials are vaild.  This tab may then be closed while the token is generated.

## Extra info
Some information and examples of the package used:
https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow
