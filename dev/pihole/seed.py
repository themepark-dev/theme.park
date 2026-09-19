#!/usr/bin/env python3
"""Add four synthetic network devices to the disposable Pi-hole database."""
import subprocess
import time
from pathlib import Path

compose = Path(__file__).with_name('compose.yaml')
now = int(time.time())
statements = []
for index, (name, age) in enumerate(
    [('recent', 60), ('today', 43200), ('older', 172800), ('never', 0)], 100
):
    last_query = now - age if age else 0
    statements.append(
        f"INSERT OR REPLACE INTO network VALUES ({index},"
        f"'02:00:00:00:00:{index:02x}','eth0',{now-604800},{last_query},42,"
        "'Synthetic device',NULL);"
    )
    statements.append(
        f"INSERT OR REPLACE INTO network_addresses VALUES ({index},"
        f"'192.0.2.{index}',{now},'sample-{name}',{now});"
    )
subprocess.run(
    ['docker', 'compose', '-f', str(compose), 'exec', '-T', 'pihole',
     'pihole-FTL', 'sqlite3', '/etc/pihole/pihole-FTL.db', ''.join(statements)],
    check=True,
)
