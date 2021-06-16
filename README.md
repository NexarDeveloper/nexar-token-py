# nexar-token-py
Getting Nexar tokens for Python.


## Installing the python packages:
Using the virtual environment manager of your choice (venv, conda, etc.), install the python packages:

`pip install -r requirements.txt`


## Importing as an external module
This repository can be imported as a submodule or subtree from another repository.

After adding the submodule/subtree it can be implemented as follows:

`from nexar_module.nexar_token import get_token`

## Obtaining Nexar token and printing to the standard output
The following command will print the Nexar token to the standard output.

You can copy it to the clipboard adding `| Set-Clipboard` for PowerShell, `| xclip -sel clip` for Bash, or `| clip.exe` for Ubuntu in WSL.

```
python print_token.py <CLIENT_ID> <CLIENT_SECRET>
python print_token.py <CLIENT_ID> <CLIENT_SECRET> | Set-Clipboard
```

## Sample request for extracting GraphQL part data
`python sample_request.py <CLIENT_ID> <CLIENT_SECRET> <MPN>`


## Extra info
Some information and examples of the package used:
https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow
