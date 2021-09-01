"""Sample workflow launch with an attached file."""
import argparse
import json
import os
import time

import requests
from nexar_token import get_token_with_login

NEXAR_URL = "https://api.nexar.com/graphql"
WORKSPACE_URL = "https://frontline-workflow.365.altium.com:443"
QUERY = """
query Workspace($workspace: String!) {
  desWorkspaces(where: {name: {eq: $workspace}}) {
    url
    name
    description
    projects {
      id
      name
      description
    }
  }
}"""

def get_nexar_query(variables, token) -> dict:
    """Return Nexar response for the query."""
    try:
        r = requests.post(
            NEXAR_URL,
            json={"query": QUERY, "variables": variables},
            headers={"token": token},
        )

        data = json.loads(r.text)["data"]["desWorkspaces"]
    except Exception:
        raise Exception("Error while getting Nexar response")
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="The client ID.", type=str)
    parser.add_argument("client_secret", help="The client secret.", type=str)
    parser.add_argument("name", help="The name for the workspace to query.", type=str)
    args = parser.parse_args()

    scopes = ["user.access", "design.domain", "supply.domain"]
    token = get_token_with_login(args.client_id, args.client_secret, scopes)["access_token"]

    variables = {
        "workspace": args.name
        }
    response = get_nexar_query(variables, token)
    print(json.dumps(response, indent = 1))
    