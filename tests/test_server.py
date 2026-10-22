# Component test: starts the real web server and sends it two requests
import json  # reads the JSON answer from /health
import threading  # runs the server in the background while the test continues
import urllib.request  # sends web requests, like curl does
from http.server import HTTPServer
 
from app import Handler  # the request handler from app.py
 
 
def test_server_answers_health_and_home_page():
    # port 0 asks the system for any free port, so the test never clashes
    server = HTTPServer(("127.0.0.1", 0), Handler)
    # start the server in the background
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"  # the test server address
    try:
        # request /health and check that the status is ok
        with urllib.request.urlopen(base + "/health") as response:
            assert json.loads(response.read())["status"] == "ok"
        # request the home page and check its heading
        with urllib.request.urlopen(base + "/") as response:
            assert "<h1>Task Tracker</h1>" in response.read().decode()
    finally:
        server.shutdown()  # always stop the server, even if a check failed
