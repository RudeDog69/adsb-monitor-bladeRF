#!/bin/bash
# Run the ADS-B Web Dashboard using the virtual environment's uvicorn.
# Assumes you are in the adsb_monitor directory.
# This script uses sudo to ensure the BladeRF can be accessed.

echo "Starting ADS-B Web Dashboard on http://0.0.0.0:8000"
echo "Press Ctrl+C to stop."

sudo ./venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000 --reload
