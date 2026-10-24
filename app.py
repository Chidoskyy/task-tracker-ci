"""app.py: Task Tracker web application."""
import json  # converts Python data into JSON text for the /health page
from http.server import BaseHTTPRequestHandler, HTTPServer  # built-in web server
 
VERSION = "1.1.0"
PORT = 8080  # the network port the web server listens on
TASKS = ["Set a budget alert", "Launch an EC2 instance", "Deploy Task Tracker"]
 
 
def health_payload():  # builds the data for the /health page
    """Return the data for the /health endpoint."""
    return {"status": "ok", "version": VERSION}  # app is up, and its version
 
 
def render_page(tasks):  # builds the HTML home page
    """Return the HTML home page for a list of tasks."""
    items = "".join(f"<li>{task}</li>" for task in tasks)  # one <li> per task
    return f"<h1>Task Tracker</h1><p>Version {VERSION}</p><ul>{items}</ul>"
 
 
def summary(tasks):  # new feature: describes how many tasks there are
    """Return a one-line summary of the task list."""
    if not tasks:  # the list is empty
        return "No tasks"
    if len(tasks) == 1:  # exactly one task, so use the singular word
        return "1 task"
    return f"{len(tasks)} tasks"  # two or more tasks
 
 
class Handler(BaseHTTPRequestHandler):  # decides how to answer each web request
    def do_GET(self):  # runs every time a browser or curl asks for a page
        if self.path == "/health":  # the request is for the health check
            body = json.dumps(health_payload()).encode()  # JSON as bytes
            content_type = "application/json"  # the answer is JSON
        else:  # any other address returns the home page
            body = render_page(TASKS).encode()  # HTML text, converted to bytes
            content_type = "text/html"  # the answer is a web page
        self.send_response(200)  # status 200 means OK
        self.send_header("Content-Type", content_type)  # describes the answer
        self.end_headers()  # finishes the headers
        self.wfile.write(body)  # sends the page itself
 
 
if __name__ == "__main__":  # true only when you run: python3 app.py
    print(f"Task Tracker {VERSION} listening on port {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()  # keep running
