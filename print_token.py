"""Sample for getting nexar token."""
import argparse
from nexar_token import get_token, get_token_with_login


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="The client ID.", type=str)
    parser.add_argument("client_secret", help="The client secret.", type=str)
    parser.add_argument("scope", help="The resources needed for authorization.", nargs="*")
    args = parser.parse_args()

    token = get_token(args.client_id, args.client_secret, args.scope)["access_token"]
    print(token)
