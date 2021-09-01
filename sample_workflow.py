"""Sample workflow launch with an attached file."""
import argparse
import json
import os
import time

import requests
from requests_toolbelt import MultipartEncoder

from nexar_token import get_token_with_login

NEXAR_URL = "https://api.nexar.com/graphql"
NEXAR_FILE_URL = "https://files.nexar.com/Upload/WorkflowAttachment"
WORKSPACE_URL = "https://frontline-workflow.365.altium.com:443"
WORKFLOW_DEFINITION = "Process_1629987953321:1:37404"
WORKFLOW_GQL = """
mutation Workflow($workspace: String!, $workflowDefinition: String!, $uploadFile: String!) {
  desLaunchWorkflow(input:{
    workspaceUrl: $workspace,
    workflowDefinitionId: $workflowDefinition,
    name: "This is optional",
    variables: [
      {name: "Description", value: "testing some new stuff"},
      {name: "PROJECT", value: "FA36A329-0650-4108-8C0B-B41DF2A3AD26"},
      {name: "Release", value: "5F1637ED-2019-4B81-9406-5D947307F56C"},
      {name: "Category", value: "General"},
      {name: "Priority", value: "Low"},
      {name: "Attachments", value: $uploadFile}
    ]}) {
    id
  }
}"""

def launch_workflow(variables, token) -> dict:
    """Return Nexar response for the new workflow."""
    try:
        r = requests.post(
            NEXAR_URL,
            json = {"query": WORKFLOW_GQL, "variables": variables},
            headers = {"token": token},
        )

        data = json.loads(r.text)["data"]["desLaunchWorkflow"]
    except Exception:
        raise Exception("Error while getting Nexar response")
    return data

def upload_file(path, container, token) -> str:
    """Return Nexar response for the file upload."""
    multipart_data = MultipartEncoder(
        fields = {
            'file': (os.path.basename(path), open(path, 'rb'), 'text/plain'),
            'workspaceUrl': WORKSPACE_URL,
            'container': container,
        }
    )

    r = requests.post(
        NEXAR_FILE_URL,
        data = multipart_data,
        headers = {
            'Content-Type': multipart_data.content_type,
            'token': token
        }
    )
    return r.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="The client ID.", type=str)
    parser.add_argument("client_secret", help="The client secret.", type=str)
    parser.add_argument("path", help="The path(s) for the file(s) to upload.", nargs="+", type=str)
    args = parser.parse_args()

    scopes = ["user.access", "design.domain", "supply.domain"]
    token = get_token_with_login(args.client_id, args.client_secret, scopes)["access_token"]

    container = str(time.time_ns()) + "-Attachment"
    response = [upload_file(path, container, token) for path in args.path]
    variables = {
        "workspace": WORKSPACE_URL,
        "workflowDefinition": WORKFLOW_DEFINITION,
        "uploadFile": ",".join(response)
        }
    print(variables)
    workflow = launch_workflow(variables, token)
    print(workflow)