"""Add three paused, synthetic queue entries to the local NZBGet test instance."""

import base64
import json
import time
from urllib.request import Request, urlopen


def rpc(method, params=None):
    # These are the disposable LinuxServer container's default credentials.
    credentials = base64.b64encode(b"nzbget:tegbzn6789").decode()
    request = Request(
        "http://localhost:16789/jsonrpc",
        json.dumps({"method": method, "params": params or [], "id": 1}).encode(),
        {
            "Content-Type": "application/json",
            "Authorization": f"Basic {credentials}",
        },
    )
    with urlopen(request, timeout=10) as response:
        result = json.load(response)
    if "error" in result:
        raise RuntimeError(result["error"])
    return result["result"]


if __name__ == "__main__":
    if not rpc("pausedownload"):
        raise RuntimeError("Could not pause downloads")
    for number in range(1, 4):
        nzb = f'''<?xml version="1.0"?>
<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">
  <file poster="test@example.invalid" date="{int(time.time())}" subject="Checkbox sample {number}.txt">
    <groups><group>alt.test</group></groups>
    <segments><segment bytes="1024" number="1">checkbox-{number}@example.invalid</segment></segments>
  </file>
</nzb>'''
        result = rpc("append", [
            f"Checkbox sample {number}.nzb",
            base64.b64encode(nzb.encode()).decode(),
            "", 0, False, True, "", 0, "ALL", [],
        ])
        if result <= 0:
            raise RuntimeError(f"Could not add sample {number}: {result}")
        print(f"Added paused sample {number} (ID {result})")
