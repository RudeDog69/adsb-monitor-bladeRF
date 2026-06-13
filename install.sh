#!/bin/bash

# ADS-B Project Installer
# This script automates the setup of the ADS-B monitoring system on Debian/Ubuntu-based systems.

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}      ADS-B Monitoring System Installer           ${NC}"
echo -e "${BLUE}====================================================${NC}"

# 1. Check for Sudo
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run with sudo.${NC}"
   exit 1
fi

# 2. Update Package Lists
echo -e "\n${BLUE}[1/5] Updating package lists...${NC}"
apt-get update -y

# 3. Install System Dependencies
echo -e "\n${BLUE}[2/5] Installing system dependencies (bladeRF, Python, etc.)...${NC}"
# We include libbladerf-dev for the bladeRF-cli and python3-venv for the virtual environment
apt-get install -y python3-venv python3-pip libbladerf-dev bladeRF-cli curl git

# 4. Create Virtual Environment
echo -e "\n${BLUE}[3/5] Setting up Python Virtual Environment...${NC}"
if [ -d "venv" ]; then
    echo "Existing venv found. Removing it to ensure a fresh install..."
    rm -rf venv
fi
python3 -m venv venv
echo "Virtual environment created."

# 5. Install Python Dependencies
echo -e "\n${BLUE}[4/5] Installing Python requirements...${NC}"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 6. Final Setup
echo -e "\n${BLUE}[5/5] Finalizing setup...${NC}"
chmod +x run_web.sh
echo "run_web.sh permissions updated."

# 7. Hardware Verification
echo -e "\n${BLUE}Verifying hardware availability...${NC}"
if bladeRF-cli --probe > /dev/null 2>&1; then
    echo -e "${GREEN}✓ bladeRF hardware detected!${NC}"
else
    echo -e "${RED}✗ bladeRF hardware NOT detected. Please check your USB connection.${NC}"
    echo "Note: The software will still run, but no RF capture will occur."
fi

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}      INSTALLATION COMPLETE!                      ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "To start the system, run:"
echo -e "    ${BLUE}./run_web.sh${NC}"
echo -e "\nIf you are in a new shell, remember to use the venv if running scripts manually."
echo -e "====================================================\n"
