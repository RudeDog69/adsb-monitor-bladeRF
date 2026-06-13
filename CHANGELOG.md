# CHANGELOG

All significant changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- **Recorder**: Fixed `bladeRF-cli` syntax (added `rx` to frequency/samplerate) and transitioned to `subprocess.run` for more robust execution.
- **Recorder**: Added strict file existence and size verification before reporting success.
- **Decoder**: Fixed `pyModeS v3` API compatibility (transitioned from function-based to dictionary-based decoding).
- **Decoder**: Implemented aggressive exponential backoff (up to 31s total wait) to solve filesystem race conditions.
- **Decoder**: Added detailed logging for retry attempts and file discovery.

### Added
- **Documentation**: Comprehensive `README.md` and `CHANGELOG.md`.
- **License**: MIT License.
- **Robustness**: Improved error handling and logging across the entire pipeline.

## [v1.0.0-dev] - 2026-06-13
- Initial project structure and implementation of ADS-B monitoring pipeline.
