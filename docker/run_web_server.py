#!/usr/bin/env python3
"""
Entrypoint for the Hermes web server in Docker.

Starts the web UI on 0.0.0.0 so it is reachable via Railway's public
networking. Browser auto-open is disabled (headless container).

Port resolution: $PORT (Railway / Heroku convention) → $HERMES_WEB_PORT →
8080. If HERMES_DASHBOARD=1 and the supervised `dashboard` s6 service is
bound to the same port, this entrypoint sleeps instead of fighting it
for the bind (otherwise uvicorn loops on EADDRINUSE).
"""

import os
import sys
import time
from pathlib import Path

# Ensure the project root is on sys.path when invoked as a plain script.
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _resolve_port() -> int:
    for var in ("PORT", "HERMES_WEB_PORT"):
        raw = os.environ.get(var)
        if raw:
            try:
                return int(raw)
            except ValueError:
                pass
    return 8080


def _dashboard_supervised_on(port: int) -> bool:
    """True if the s6 dashboard service is already serving on `port`."""
    if os.environ.get("HERMES_DASHBOARD", "").lower() not in {"1", "true", "yes"}:
        return False
    dash_port_raw = os.environ.get("HERMES_DASHBOARD_PORT", "9119")
    try:
        return int(dash_port_raw) == port
    except ValueError:
        return False


if __name__ == "__main__":
    port = _resolve_port()

    if _dashboard_supervised_on(port):
        print(
            f"  HERMES_DASHBOARD=1 already serves on port {port}; "
            f"run_web_server.py going idle.",
            flush=True,
        )
        while True:
            time.sleep(3600)

    from hermes_cli.web_server import start_server

    start_server(
        host="0.0.0.0",
        port=port,
        open_browser=False,
        allow_public=True,
    )
