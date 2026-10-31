"""Seed SABnzbd with sample jobs and warnings for theme development.

Usage:
  seed.py             add sample jobs, then create warnings
  seed.py --warnings  only recreate warnings, for example after a restart

The sample jobs are one that completes, one whose articles are missing so it
fails, and a paused job that stays in the queue. SABnzbd keeps warnings in
memory, so recreating the container clears them.

The warnings come from the fake-nntp server, which answers with a 502.
SABnzbd waits for that server's penalty to expire before it gives up on an
article, so the script turns the server off once a warning exists. Without
that step the failing job stays in the queue for several minutes.
"""

import json
import sys
import time
import urllib.parse
import urllib.request
import uuid

API = "http://localhost:18080/api"
KEY = "themeparkdevapikey00000000000000"
PAUSED = -2

FILE = """  <file poster="dev@example.com" date="1700000000" subject="&quot;{name}&quot; yEnc ({n}/{total})">
    <groups><group>alt.binaries.test</group></groups>
    <segments><segment bytes="{size}" number="1">{msgid}@example.com</segment></segments>
  </file>
"""

NZB = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.1//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.1.dtd">
<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">
{files}</nzb>
"""


def build_nzb(job: str, files: int, size: int, missing: bool = False) -> str:
    tag = uuid.uuid4().hex[:8]
    entries = []
    for n in range(1, files + 1):
        msgid = f"{job}-{tag}-{n}" + ("-missing" if missing else "")
        entries.append(FILE.format(name=f"{job}.part{n}.bin", n=n, total=files, size=size, msgid=msgid))
    return NZB.format(files="".join(entries))


def add_nzb(job: str, nzb: str, priority: int | None = None) -> dict:
    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="name"; filename="{job}.nzb"\r\n'
        "Content-Type: application/x-nzb\r\n\r\n"
        f"{nzb}\r\n"
        f"--{boundary}--\r\n"
    ).encode()
    params = {"mode": "addfile", "output": "json", "apikey": KEY}
    if priority is not None:
        params["priority"] = str(priority)
    request = urllib.request.Request(
        f"{API}?{urllib.parse.urlencode(params)}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def api(**params: str) -> dict:
    query = urllib.parse.urlencode({**params, "output": "json", "apikey": KEY})
    with urllib.request.urlopen(f"{API}?{query}") as response:
        return json.load(response)


def wait_for(check, timeout: float, what: str) -> None:
    deadline = time.monotonic() + timeout
    while not check():
        if time.monotonic() > deadline:
            sys.exit(f"Timed out waiting for {what}")
        time.sleep(2)


def set_reject_server(enabled: bool) -> None:
    api(mode="set_config", section="servers", keyword="fake-nntp", enable=str(int(enabled)))


def create_warnings() -> None:
    """Queue a throwaway job while the 502 server is on, then remove both."""
    set_reject_server(True)
    nzo_ids = add_nzb("themepark-warning", build_nzb("themepark-warning", 1, 17000, missing=True))["nzo_ids"]
    wait_for(lambda: api(mode="warnings")["warnings"], 90, "a warning")
    for nzo_id in nzo_ids:
        api(mode="queue", name="delete", value=nzo_id, del_files="1")
    set_reject_server(False)
    print(f"{len(api(mode='warnings')['warnings'])} warning(s)")


def history_names() -> list[str]:
    return [slot["name"] for slot in api(mode="history")["history"]["slots"]]


if __name__ == "__main__":
    if "--warnings" not in sys.argv:
        # The fake server returns 16 KiB per article, which is about 17 KB encoded.
        print(add_nzb("themepark-complete", build_nzb("themepark-complete", 3, 17000)))
        print(add_nzb("themepark-missing", build_nzb("themepark-missing", 2, 17000, missing=True)))
        # Glitter will not open the Files modal for a job it reports as 0.00 MB.
        print(add_nzb("themepark-queued", build_nzb("themepark-queued", 3, 2000000), PAUSED))
    create_warnings()
    if "--warnings" not in sys.argv:
        wait_for(lambda: "themepark-missing" in history_names(), 180, "the failed job")
        print("history:", history_names())
