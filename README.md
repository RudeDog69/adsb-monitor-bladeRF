# ADS-B Monitoring System

A Python-based ADS-B monitoring system designed for the Nuand bladeRF 2.0 SDR. This system captures, decodes, and visualizes nearby aircraft traffic via a web-based dashboard.

## 🚀 Features
- **Real-time RF Capture**: Uses `bladeRF-cli` to capture raw IQ samples at 1090 MHz.
- **Robust Decoding**: Implements `pyModeS v3` for reliable Mode S message decoding.
- **Web Dashboard**: A FastAPI-powered web interface with real-time aircraft tracking and map visualization.
- **Resilient Engine**: Automated retry logic and exponential backoff to handle hardware/filesystem latency.
- **Logging**: Comprehensive logging for both hardware capture and software decoding stages.

## 🛠 Hardware Requirements
- **SDR**: Nuand bladeRF 2.0 (or compatible).
- **Antenna**: High-gain 1090 MHz tuned antenna (recommended).
- **Connection**: USB 3.0 connection for stable data throughput.

## 💻 Software Requirements
- Python 3.12+
- `bladeRF-cli` (with FPGA loaded)
- Python Packages:
  - `numpy`
    - `pyModeS` (v3)
  - `fastapi`
  - `uvicorn`
  - `jinja2`
  - `httpx`

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd adsb_monitor
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure BladeRF:**
   Ensure `bladeRF-cli` is installed and your FPGA bitstream is located at `/usr/share/Nuand/bladeRF/hostedxA4.rbf` (or update `recorder.py`).

4. **Run the system:**
   ```bash
   chmod +x run_web.sh
   ./run_web.sh
   ```

## 📜 License
This project is licensed under the MIT License.
