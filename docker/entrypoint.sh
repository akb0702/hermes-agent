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

# Start the main process
exec /init /opt/hermes/docker/main-wrapper.sh

