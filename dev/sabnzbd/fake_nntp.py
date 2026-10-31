"""Minimal NNTP stand-in for SABnzbd theme development.

MODE=reject answers every connection with a 502 so SABnzbd logs warnings.
MODE=serve returns a small yEnc body for every article, except message IDs
containing "missing", which get a 430 so the job fails.
"""

import os
import socketserver
import zlib

MODE = os.environ.get("MODE", "reject")
PAYLOAD = bytes(range(256)) * 64  # 16 KiB per article


def yenc(data: bytes, name: str) -> bytes:
    """Encode one single-part yEnc article body, dot-stuffed for NNTP."""
    lines, line = [], bytearray()
    for byte in data:
        out = (byte + 42) % 256
        if out in (0x00, 0x0A, 0x0D, 0x3D) or (not line and out in (0x09, 0x20, 0x2E)):
            line += bytes((0x3D, (out + 64) % 256))
        else:
            line.append(out)
        if len(line) >= 128:
            lines.append(bytes(line))
            line = bytearray()
    if line:
        lines.append(bytes(line))
    crc = zlib.crc32(data) & 0xFFFFFFFF
    head = f"=ybegin line=128 size={len(data)} name={name}".encode()
    tail = f"=yend size={len(data)} crc32={crc:08x}".encode()
    return b"\r\n".join([head, *lines, tail]) + b"\r\n.\r\n"


class Handler(socketserver.StreamRequestHandler):
    def send(self, text: str) -> None:
        self.wfile.write(text.encode() + b"\r\n")

    def handle(self) -> None:
        if MODE == "reject":
            self.send("502 connection limit (50) reached")
            return
        self.send("200 theme.park fake NNTP ready")
        for raw in self.rfile:
            parts = raw.decode(errors="replace").strip().split()
            if not parts:
                continue
            cmd, args = parts[0].upper(), parts[1:]
            if cmd == "QUIT":
                self.send("205 bye")
                return
            if cmd in ("BODY", "ARTICLE"):
                msgid = args[0] if args else "<none>"
                if "missing" in msgid:
                    self.send("430 no such article")
                    continue
                code = 222 if cmd == "BODY" else 220
                self.send(f"{code} 0 {msgid}")
                name = msgid.strip("<>").split("@")[0] + ".bin"
                self.wfile.write(yenc(PAYLOAD, name))
            elif cmd == "STAT":
                self.send(f"223 0 {args[0] if args else ''}")
            elif cmd == "DATE":
                self.send("111 20261031000000")
            elif cmd == "MODE":
                self.send("200 reader")
            elif cmd == "GROUP":
                self.send(f"211 0 0 0 {args[0] if args else ''}")
            elif cmd == "CAPABILITIES":
                self.send("101 capabilities")
                self.send("VERSION 2")
                self.send("READER")
                self.send(".")
            else:
                self.send("500 unknown command")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


with Server(("0.0.0.0", 119), Handler) as server:
    server.serve_forever()
