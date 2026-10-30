#!/bin/bash
# ==============================================================
# CC WiFi Smart Radio Bridge - Debian/Linux One-Step Installer
# Host: 192.168.1.68
# ==============================================================
set -e

echo "=== Installing dependencies (Python 3, Flask, Requests) ==="
apt-get update
apt-get install -y python3 python3-flask python3-requests

echo "=== Setting up /opt/ccwifi-bridge directory ==="
mkdir -p /opt/ccwifi-bridge/templates

# Copy files if running from extracted package
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/app.py" /opt/ccwifi-bridge/
cp "$SCRIPT_DIR/config.json" /opt/ccwifi-bridge/
cp "$SCRIPT_DIR/templates/index.html" /opt/ccwifi-bridge/templates/

echo "=== Registering and starting systemd service ==="
cp "$SCRIPT_DIR/ccwifi-bridge.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable ccwifi-bridge.service
systemctl restart ccwifi-bridge.service

echo ""
echo "=========================================================="
echo " CC WiFi Bridge is now RUNNING on your server 24/7!"
echo " Web UI: http://192.168.1.68:5000"
echo "=========================================================="
systemctl status ccwifi-bridge --no-pager
