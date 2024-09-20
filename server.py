import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import time


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/pr_explorer.html"
        return SimpleHTTPRequestHandler.do_GET(self)


class PRExplorerHandler(SimpleHTTPRequestHandler):
    def send_cacheable_response(
        self, content, content_type="application/json", last_modified=None
    ):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Cache-Control", "public, max-age=3600")  # Cache for 1 hour
        if last_modified:
            self.send_header("Last-Modified", self.date_time_string(last_modified))
        self.end_headers()
        self.wfile.write(content.encode())

    def do_GET(self):
        if self.path == "/":
            with open("pr_explorer.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
            return
        elif self.path == "/list_files":
            repos = []
            for root, _dirs, files in os.walk("dataset"):
                for file in files:
                    if (
                        file.endswith("-task-instances.jsonl")
                        and os.path.basename(root) != "dataset"
                    ):
                        repo_name = os.path.basename(root)
                        repos.append(repo_name)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(json.dumps(repos).encode())
            return
        elif self.path.startswith("/instances/"):
            repo = self.path[11:]  # Remove leading /instances/
            file_path = f"dataset/{repo}/{repo}-task-instances.jsonl"
            if os.path.exists(file_path):
                last_modified = os.path.getmtime(file_path)
                if_modified_since = self.headers.get("If-Modified-Since")

                if if_modified_since:
                    if_modified_since = time.mktime(
                        time.strptime(if_modified_since, "%a, %d %b %Y %H:%M:%S GMT")
                    )
                    if last_modified <= if_modified_since:
                        self.send_response(304)
                        self.end_headers()
                        return

                with open(file_path, "rb") as f:
                    instances_data = [json.loads(line.strip()) for line in f]
                    response_data = {
                        "repository": instances_data[0]["repo"],
                        "repo_short": repo,
                        "issues": instances_data,
                    }
                self.send_cacheable_response(
                    json.dumps(response_data), last_modified=last_modified
                )
                return
        return SimpleHTTPRequestHandler.do_GET(self)


def run_server():
    port = 80
    httpd = HTTPServer(("0.0.0.0", port), PRExplorerHandler)
    print(f"Serving at http://116.203.88.45:{port}")
    print("Press Ctrl+C to stop the server")
    webbrowser.open(f"http://116.203.88.45:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    run_server()
