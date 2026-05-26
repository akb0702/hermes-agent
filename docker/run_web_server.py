#!/usr/bin/env python
"""Start Hermes web server."""
import sys
sys.path.insert(0, '/opt/hermes')

from hermes_cli.web_server import start_server

if __name__ == '__main__':
    start_server(host='0.0.0.0', port=8080)

