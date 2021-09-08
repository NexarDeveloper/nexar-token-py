"""Sample for getting nexar token."""
import argparse
import pyperclip

from nexar_token import get_token


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="The client ID.", type=str)
    parser.add_argument("client_secret", help="The client secret.", type=str)
    args = parser.parse_args()

    token = get_token(args.client_id, args.client_secret)["access_token"]
    pyperclip.copy(token)
    print("Your token has been copied to the clipboard")
