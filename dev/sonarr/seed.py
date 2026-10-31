#!/usr/bin/env python3
"""Prepare the disposable Sonarr instances in dev/sonarr/compose.yaml.

Usage, from the repository root after `docker compose ... up -d`:
    python3 -I dev/sonarr/seed.py            # both v4 and v5
    python3 -I dev/sonarr/seed.py v5         # one service

For each service the script:
  * enables Forms login with admin / admin,
  * adds /tv as a root folder,
  * adds a few series using Sonarr's public metadata lookup,
  * writes empty placeholder files for some episodes and rescans, so the UI
    shows downloaded, missing, and unaired states.

It adds no indexers or download clients and downloads nothing. Running it
again skips series that already exist.
"""

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

COMPOSE = ["docker", "compose", "-f", str(Path(__file__).with_name("compose.yaml"))]
PORTS = {"v4": 18989, "v5": 18990}
# tvdb id, folder name, seasons that get placeholder files
SERIES = [
    (81189, "Breaking Bad (2008)", [1, 2, 3, 4, 5]),
    (371980, "Severance (2022)", [1]),
    (71663, "The Simpsons (1989)", [1, 2]),
    (305288, "Stranger Things (2016)", []),
]


def compose(*args, user=None):
    cmd = COMPOSE + ["exec", "-T"] + (["-u", user] if user else []) + list(args)
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def api(base, key, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{base}/api/v3/{path}",
        data=data,
        method=method,
        headers={"X-Api-Key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else None


def wait_ready(base, key):
    for _ in range(60):
        try:
            return api(base, key, "GET", "system/status")
        except (urllib.error.URLError, ConnectionError):
            time.sleep(2)
    raise SystemExit(f"{base} did not become ready")


def seed(service):
    base = f"http://127.0.0.1:{PORTS[service]}"
    key = compose(service, "sh", "-c", "sed -n 's:.*<ApiKey>\\(.*\\)</ApiKey>.*:\\1:p' /config/config.xml").strip()
    status = wait_ready(base, key)
    print(f"{service}: Sonarr {status['version']} at {base}")

    host = api(base, key, "GET", "config/host")
    host.update(
        authenticationMethod="forms",
        authenticationRequired="enabled",
        username="admin",
        password="admin",
        passwordConfirmation="admin",
    )
    api(base, key, "PUT", f"config/host/{host['id']}", host)
    print("  login: admin / admin")

    compose(service, "chown", "abc:users", "/tv", user="root")
    if not any(r["path"] == "/tv" for r in api(base, key, "GET", "rootfolder")):
        api(base, key, "POST", "rootfolder", {"path": "/tv"})

    profile = api(base, key, "GET", "qualityprofile")[0]["id"]
    existing = {s["tvdbId"] for s in api(base, key, "GET", "series")}
    for tvdb, folder, seasons in SERIES:
        if tvdb not in existing:
            found = api(base, key, "GET", f"series/lookup?term=tvdb:{tvdb}")
            if not found:
                print(f"  lookup failed for tvdb:{tvdb}")
                continue
            series = found[0]
            series.update(
                qualityProfileId=profile,
                rootFolderPath="/tv",
                path=f"/tv/{folder}",
                monitored=True,
                seasonFolder=True,
                addOptions={"monitor": "all", "searchForMissingEpisodes": False},
            )
            api(base, key, "POST", "series", series)
            print(f"  added {series['title']}")
        if seasons:
            script = "".join(
                f"mkdir -p '/tv/{folder}/Season {n:02d}' && "
                f"for e in $(seq -w 1 13); do : > '/tv/{folder}/Season {n:02d}/{folder} - S{n:02d}E'$e' - WEBDL-1080p.mkv'; done && "
                for n in seasons
            )
            compose(service, "sh", "-c", script + "chown -R abc:users /tv", user="root")
    api(base, key, "POST", "command", {"name": "RescanSeries"})
    print("  placeholder files written; rescan queued")


def main(argv):
    for service in argv[1:] or list(PORTS):
        seed(service)


if __name__ == "__main__":
    main(sys.argv)
