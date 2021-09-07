"""Main entry point to the service."""
import http.server
from urllib.parse import parse_qs, urlparse

HOST_NAME = "localhost"
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

def handlerFactory(code):
    class MyHandler(http.server.BaseHTTPRequestHandler):
        def log_request(code='-', size='-'):
            pass
        def do_HEAD(s):
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
        def do_GET(s):
            """Respond to a GET request."""
            o = urlparse(s.path)
            response = parse_qs(o.query)

            if (o.path != "/login"): return

            if ("code" not in response):
                s.send_response(400)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write(HTML_400.encode())
                code.append("invalid")
                return

            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(HTML_200.encode())
            code.append(response["code"][0])
    return MyHandler

def run(q):
    code = []
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT), handlerFactory(code))

    while (len(code) == 0):
        httpd.handle_request()

    q.put(code[0])
    httpd.server_close()
