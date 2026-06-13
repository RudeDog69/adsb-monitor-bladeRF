import subprocess
import subprocess
import logging
import os
import time

logger = logging.getLogger(__name__)

class BladeRFRecorder:
    def __init__(self, frequency=109000000, samplerate=2000000, file_path="/tmp/adsb_capture.bin", fpga_path="/usr/share/Nuand/bladeRF/hostedxA4.rbf"):
        self.frequency = frequency
        self.samplerate = samplerate
        self.file_path = file_path
        self.fpga_path = fpga_path
        self.process = None

    def start(self):
        logger.info(f"Starting BladeRF capture at {self.frequency} Hz, {self.samplerate} Hz -> {self.file_path}")
        
        # Using the non-deprecated syntax found in manual testing
        cmd = [
            "sudo", "bladeRF-cli",
            "-e", f"load fpga {self.fpga_path}",
            "-e", f"set frequency rx {self.frequency}",
            "-e", f"set samplerate rx {self.samplerate}",
            "-e", f"rx config file={self.file_path} format=bin",
            "-e", "rx start",
            "-e", "rx wait"
        ]
        
        try:
            # Use subprocess.run for a synchronous, robust call
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Ensure the file is flushed and accessible
                time.sleep(2)
                if os.path.exists(self.file_path):
                    try:
                        subprocess.run(["sudo", "chmod", "666", self.file_path], check=True)
                        logger.info(f"Permissions updated for {self.file_path}")
                    except Exception as e:
                        logger.error(f"Failed to set permissions on {self.file_path}: {e}")
                
                # Final check: Did the file actually get created and have content?
                if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
                    logger.info(f"Capture completed successfully. File size: {os.path.getsize(self.file_path)} bytes")
                    return True
                else:
                    logger.error(f"Capture reported success, but file {self.file_path} is empty or missing.")
                    return False
            else:
                logger.error(f"Capture failed with return code {result.returncode}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Capture command timed out.")
            return False
        except Exception as e:
            logger.error(f"Error during capture: {e}")
            return False

    def stop(self):
        # Since we switched to subprocess.run, 'stop' is handled by the completion of the command.
        # For long-running background processes, this would need a different approach,
        # but since our engine loop waits for the capture burst to complete, 
        # the command itself manages the lifecycle.
        logger.info("Stop requested (not applicable in synchronous mode).")

