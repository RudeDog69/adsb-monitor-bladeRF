# Hardware Specifications & Notes

## 📡 RF Requirements
- **Frequency**: 1090 MHz (ADS-B standard).
- **Target Signal**: Mode S (Extended Squitter) aircraft broadcasts.

## 🛠 Hardware Components
- **SDR**: Nuand bladeRF 2.0 micro.
- **Interface**: USB 3.0.
- **Current Status**: Testing with existing antenna; awaiting upgrade (new antenna + USB extension).

## ⚙️ BladeRF Configuration
- **Sample Rate**: 2,000,000 Hz (2 MSPS).
- **Frequency Setting**: `set frequency rx 109000000` (Note: `rx` prefix required).
- **FPGA Bitstream**: `/usr/share/Nuand/bladeRF/hostedxA4.rbf`.

## ⚠️ Known Issues
- USB connection stability: Requires high-quality cables and proximity to the host for consistent capture.
- RF interference: Local 1GHz noise can degrade signal; antenna placement is critical.
