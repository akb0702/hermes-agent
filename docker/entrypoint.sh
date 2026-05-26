#!/bin/sh
set -e

# Create config directory
mkdir -p /opt/data/.hermes

# Write config file
cat > /opt/data/.hermes/config.yaml << 'EOF'
model:
  default: openrouter/meta-llama/llama-3.1-70b-instruct
  provider: openrouter
EOF

# Write .env file with API key
cat > /opt/data/.hermes/.env << EOF
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
EOF

# Start Hermes web server via Python
exec /opt/hermes/.venv/bin/python << 'PYEOF'
import sys
sys.path.insert(0, '/opt/hermes')
from hermes_cli.web_server import start_server
start_server(host='0.0.0.0', port=8080)
PYEOF

