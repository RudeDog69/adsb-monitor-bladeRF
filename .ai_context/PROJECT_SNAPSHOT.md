# Project Snapshot

This file provides a high-level overview of the current project state for incoming agents.

## 📌 Current Status
- **Project Name:** ADS-B Monitoring System
- **Stability:** Functional (Software-wise), pending Hardware verification.
- **Key Blockers:** RF signal/Antenna quality.
- **Last Major Change:** Upgraded installer to support Systemd and improved documentation.

## 🛠 Working Directory Structure
- `adsb_monitor/`
    - `.ai_context/`: Knowledge base for agents.
    - `install.sh`: Automated deployment script.
    - `engine.py`: Main orchestration loop.
    - `recorder.py`: BladeRF hardware capture logic.
    - `decoder.py`: Mode S decoding logic.
    - `server.py`: FastAPI web backend.
    - `run_web.sh`: Entry point for the application.
    - `requirements.txt`: Python dependencies.
    - `README.md`: User documentation.

## 🚀 Next Steps
1.  **Hardware Test**: Verify signal strength with new antenna/cables.
2.  **Feature Expansion**: (e.g., adding more telemetry, improved map layers).
3.  **CI/CD**: Automating tests via GitHub Actions.

## 📋 Ongoing Tasks
- [ ] Improve RF signal capture via hardware upgrade.
- [ ] Refine real-time map rendering performance.
