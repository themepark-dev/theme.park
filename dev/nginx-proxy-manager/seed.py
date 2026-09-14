"""Add two disposable proxy hosts to the local NPM review instance."""
import json
import os
import urllib.request

BASE = "http://127.0.0.1:18084/api"


def request(path, payload=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None if payload is None else json.dumps(payload).encode()
    with urllib.request.urlopen(urllib.request.Request(BASE + path, data, headers)) as response:
        return json.load(response)


token = request("/tokens", {"identity": "admin@example.com", "secret": os.environ.get("NPM_DEV_PASSWORD", "adminadmin")})["token"]
existing = {domain for host in request("/nginx/proxy-hosts", token=token) for domain in host["domain_names"]}
for domain in ("media.example.test", "downloads.example.test"):
    if domain not in existing:
        request("/nginx/proxy-hosts", {
            "domain_names": [domain], "forward_scheme": "http",
            "forward_host": "css", "forward_port": 8000,
            "access_list_id": 0, "certificate_id": 0,
            "ssl_forced": False, "caching_enabled": False,
            "block_exploits": False, "allow_websocket_upgrade": False,
            "http2_support": False, "advanced_config": "", "locations": [],
            "meta": {},
        }, token)
        print(f"Created {domain}")

if not any(user["email"] == "reviewer@example.test" for user in request("/users", token=token)):
    request("/users", {
        "name": "Theme Reviewer", "nickname": "Reviewer",
        "email": "reviewer@example.test", "roles": [], "is_disabled": False,
    }, token)
    print("Created the review user for permission-dialog checks")
