#!/bin/bash

# ADS-B Project Installer & Service Configurator
# This script automates the setup of the ADS-B monitoring system and configures it as a systemd service.

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}      ADS-B System Installer & Service Setup       ${NC}"
echo -e "${BLUE}====================================================${NC}"

# 1. Check for Sudo
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run with sudo to install packages and configure services.${NC}"
   exit 1
fi

# Get the real user (the one who called sudo) to use for service ownership
REAL_USER=$(logname)
USER_HOME=$(getent passwd "$REAL_USER" | cut -d: -f5 | sed 's/\/$//')
PROJECT_DIR=$(pwd)

# 2. Update Package Lists
echo -e "\n${BLUE}[1/6] Updating package lists...${NC}"
apt-get update -y

# 3. Install System Dependencies
echo -e "\n${BLUE}[2/6] Installing system dependencies (bladeRF, Python, etc.)...${NC}"
apt-get install -y python3-venv python3-pip libbladerf-dev bladeRF-cli curl git systemd

# 4. Create Virtual Environment
echo -e "\n${BLUE}[3/6] Setting up Python Virtual Environment...${NC}"
if [ -d "venv" ]; then
    echo "Existing venv found. Removing it to ensure a fresh install..."
    rm -rf venv
fi
python3 -m venv venv
echo "Virtual environment created."

# 5. Install Python Dependencies
echo -e "\n${BLUE}[4/6] Installing Python requirements...${NC}"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 6. Configure Systemd Service
echo -e "\n${BLUE}[5/6] Configuring Systemd Service (Auto-start on boot)...${NC}"

SERVICE_FILE="/etc/systemd/system/adsb-monitor.service"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=ADS-B Monitoring System (BladeRF)
After=network.target

[Service]
Type=simple
User=$REAL_USER
WorkingDirectory=$PROJECT_DIR
Environment="PYTHONPATH=$PROJECT_DIR"
ExecStart=$PROJECT_DIR/run_web.sh
Restart=always
RestartSec=5
StandardOutput=append:$PROJECT_DIR/logs/systemd-service.log
StandardError=append:$PROJECT_DIR/logs/systemd-service.log

[Install]
WantedBy=multi-user.target
EOF

echo "Service file created at $SERVICE_FILE"
systemctl daemon-reload
systemctl enable adsb-monitor.service
echo "Service enabled (will start on next boot)."

# 7. Final Hardware Verification
echo -e "\n${BLUE}[6/6] Finalizing setup...${NC}"
chmod +x run_web.sh
echo "run_web.sh permissions updated."

if bladeRF-cli --probe > /dev/null 2>&1; then
    echo -e "${GREEN}✓ bladeRF hardware detected!${NC}"
else
    echo -e "${RED}✗ bladeRF hardware NOT detected. Please check your USB connection.${NC}"
    echo "Note: The service will still run, but RF capture will fail until hardware is connected."
fi

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}      INSTALLATION & SERVICE SETUP COMPLETE!       ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "Commands to manage your service:"
echo -e "    ${BLUE}sudo systemctl start adsb-monitor${NC}    (Start now)"
echo -e "    ${BLUE}sudo systemctl stop adsb-monitor${NC}     (Stop)"
echo -e "    ${BLUE}sudo systemctl status adsb-monitor${NC}    (Check status)"
echo -e "    ${BLUE}journalctl -u adsb-monitor -f${NC}        (View logs)"
echo -e "\n====================================================\n"
