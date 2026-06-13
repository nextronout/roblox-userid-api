from http.server import BaseHTTPRequestHandler
import json, os, re, requests
from urllib.parse import quote

PASSWORD = os.environ.get("SETUP_PASSWORD")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))

            if data.get("password") != PASSWORD:
                return self.send_json(401, {"ok": False, "code": 401, "reason": "Invalid password"})

            username = data.get("username")
            if not username:
                return self.send_json(400, {"ok": False, "code": 400, "reason": "Missing username"})

            r = requests.get(
                "https://www.roblox.com/users/profile?username=" + quote(username),
                allow_redirects=False,
                timeout=10
            )

            location = r.headers.get("Location", "")

            user_match = re.search(r"/users/(\d+)/profile", location)
            if user_match:
                return self.send_json(200, {
                    "ok": True,
                    "code": 200,
                    "userId": int(user_match.group(1)),
                    "profile": location
                })

            error_match = re.search(r"code=(\d+)", location)
            if error_match:
                code = int(error_match.group(1))
                return self.send_json(200, {
                    "ok": False,
                    "code": code,
                    "reason": "Roblox returned an error",
                    "redirect": location
                })

            return self.send_json(200, {
                "ok": False,
                "code": r.status_code,
                "reason": "Unknown Roblox response",
                "redirect": location
            })

        except Exception as e:
            return self.send_json(500, {"ok": False, "code": 500, "reason": str(e)})

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())