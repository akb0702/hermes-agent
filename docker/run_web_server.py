#!/usr/bin/env python3
"""
Entrypoint for the Hermes web server in Docker.

Starts the web UI on 0.0.0.0:8080 so it is reachable via Railway's
public networking. Browser auto-open is disabled (headless container).
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path when invoked as a plain script.
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hermes_cli.web_server import start_server

if __name__ == "__main__":
    start_server(
        host="0.0.0.0",
        port=8080,
        open_browser=False,
        allow_public=True,
    )
