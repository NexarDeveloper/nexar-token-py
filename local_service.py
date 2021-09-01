"""Main entry point to the service."""
from flask import Flask, make_response, request
from waitress import serve

app = Flask(__name__)
code = ""

PORT = 3000
REDIRECT_URI = "http://localhost:3000/login"
AUTHORITY_URL = "https://identity.nexar.com/connect/authorize"
PROD_TOKEN_URL = "https://identity.nexar.com/connect/token"
HTML_400 = "<h1>Invalid request.</h1>"
HTML_200 = """
<html>
<head>
  <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
  <title>Welcome to Nexar</title>
  <style>
    html {
      height: 100%;
      background-image: linear-gradient(to right, #000b24, #001440);
    }
    body {
      color: #ffffff;
    }
    .center {
      width: 100%;
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
    }
    .title {
      font-family: Montserrat, sans-serif;
      font-weight: 400;
    }
    .normal {
      font-family: Montserrat, sans-serif;
      font-weight: 300;
    }
  </style>
</head>
<body>
  <div class="center">
    <h1 class="title">Welcome to Nexar</h1>
    <p class="normal">You can now return to the application.</p>
  </div>
</body>
</html>
"""


@app.route("/login", methods=["GET"])
def login():
    """Show login page."""
    global code
    if request.args is None:
        code = "invalid"
        return make_response(HTML_400, 400)
    else:
        code = request.args.get("code")
        return make_response(HTML_200, 200)

@app.route("/authcode", methods=["GET"])
def authcode():
  return code

def main():
    """Start the service."""
    return serve(app, host="localhost", port=PORT)
