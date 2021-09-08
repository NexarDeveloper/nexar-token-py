"""Sample for getting nexar token with login."""
import argparse
import pyperclip

from nexar_token import get_token_with_login


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="The client ID.", type=str)
    parser.add_argument("client_secret", help="The client secret.", type=str)
    parser.add_argument("scope", help="The scope.", nargs="*", default = ["user.access", "design.domain", "supply.domain"])
    args = parser.parse_args()

    token = get_token_with_login(args.client_id, args.client_secret, args.scope)["access_token"]
    pyperclip.copy(token)
    print("Your token has been copied to the clipboard")
