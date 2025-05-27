from mail_parser import parse_eml
import tempfile
import os

SAMPLE = """From: alice@example.com
To: bob@example.com
Subject: Hallo
Message-ID: <1@example.com>

Hallo Bob,
das ist eine Testmail.
"""

with tempfile.NamedTemporaryFile(delete=False, suffix=".eml") as f:
    f.write(SAMPLE.encode())
    path = f.name

info = parse_eml(path)
print(info["subject"])
print(info["from"])
os.unlink(path)
