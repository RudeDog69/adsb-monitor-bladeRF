# Architectural Decisions (ADR)

This file documents the "Why" behind technical decisions to maintain consistency across agent sessions.

## [ADR-001] Transition to pyModeS v3
**Date:** 2026-06-13
**Status:** Accepted
**Context:** The project was using `pyModeS.adsb` which was removed in v3.
**Decision:** Refactor `decoder.py` to use the dictionary-based API (e.g., `decoded.get('icao')`) instead of attempting to downgrade the library.
**Consequence:** Ensures long-term compatibility with modern Python environments and avoids dependency hell.

## [ADR-002] Synchronous Capture via subprocess.run
**Date:** 2026-06-13
**Status:** Accepted
**Context:** `subprocess.Popen` was causing race conditions where the recorder reported success before the file was actually flushed/available.
**Decision:** Use `subprocess.run` with a defined timeout and explicit `time.sleep` for kernel/filesystem flushing.
**Consequence:** Increased reliability of the capture-to-decode pipeline, though slightly higher latency in the loop.

## [ADR-003] Systemd Service Integration
**Date:** 2026-06-13
**Status:** Accepted
**Context:** User requires the system to run as a background service that survives reboots.
**Decision:** Implement an automated `install.sh` that generates a systemd unit file.
**Consequence:** Simplifies deployment on new machines and provides native OS-level management (start/stop/restart).
