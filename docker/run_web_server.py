#!/usr/bin/env python3
"""
Entrypoint for the Hermes web server in Docker.

Starts the web UI on 0.0.0.0 so it is reachable via Railway's public
networking. Browser auto-open is disabled (headless container).

Port resolution: $PORT (Railway / Heroku convention) → $HERMES_WEB_PORT →
8080. If something else is already bound to the chosen port (typically
the supervised `hermes dashboard` s6 service when HERMES_DASHBOARD=1),
this script sleeps forever instead of crash-looping on EADDRINUSE — the
process that wins the bind serves traffic, and Railway routes to it.
"""

import os
import socket
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


def _port_is_free(port: int) -> bool:
    """Probe whether we can bind 0.0.0.0:port right now.

    Tries an actual bind so we detect anything holding the port, not just
    LISTEN sockets. Releases the probe socket immediately.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
    except OSError:
        return False
    finally:
        s.close()
    return True


def _sleep_forever(reason: str) -> None:
    print(f"  run_web_server.py: {reason} — going idle.", flush=True)
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    port = _resolve_port()

    if not _port_is_free(port):
        _sleep_forever(
            f"port {port} already bound by another process (likely the "
            f"supervised hermes dashboard service)"
        )

    from hermes_cli.web_server import start_server

    start_server(
        host="0.0.0.0",
        port=port,
        open_browser=False,
        allow_public=True,
    )
