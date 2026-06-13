import subprocess
import logging
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_recorder")

class BladeRFRecorder:
    def __init__(self, frequency=109000000, samplerate=2000000, file_path="/tmp/adsb_capture.bin", fpga_path="/usr/share/Nuand/bladeRF/hostedxA4.rbf"):
        self.frequency = frequency
        self.samplerate = samplerate
        self.file_path = file_path
        self.fpga_path = fpga_path
        self.process = None

    def start(self):
        logger.info(f"Starting BladeRF capture at {self.frequency} Hz, {self.samplerate} Hz -> {self.file_path}")
        cmd = [
            "sudo", "bladeRF-cli",
            "-e", f"load fpga {self.fpga_path}",
            "-e", f"set frequency {self.frequency}",
            "-e", f"set samplerate {self.samplerate}",
            "-e", f"rx config file={self.file_path} format=bin",
            "-e", "rx start",
            "-e", "rx wait"
        ]
        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = self.process.communicate()
            
            time.sleep(2)  # Ensure kernel flush
            
            if self.process.returncode == 0:
                if os.path.exists(self.file_path):
                    try:
                        subprocess.run(["sudo", "chmod", "666", self.file_path], check=True)
                        logger.info(f"Permissions updated for {self.file_path}")
                    except Exception as e:
                        logger.error(f"Failed to set permissions on {self.file_path}: {e}")
                
                logger.info("Capture completed successfully.")
                return True
            else:
                logger.error(f"Capture failed: {stderr}")
                return False
        except Exception as e:
            logger.error(f"Error during capture: {e}")
            return False

    def stop(self):
        if self.process:
            self.process.terminate()
            logger.info("Capture stopped.")

def test_capture():
    file_path = "/tmp/test_recorder_capture.bin"
    if os.path.exists(file_path):
        os.remove(file_path)
        
    recorder = BladeRFRecorder(file_path=file_path)
    
    logger.info("Starting test capture...")
    success = recorder.start()
    
    if success:
        logger.info(f"Capture reported success. Checking file: {file_path}")
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            logger.info(f"File size: {size} bytes")
            if size > 0:
                logger.info("Success! File has content.")
            else:
                logger.error("Failure! File is 0 bytes.")
        else:
            logger.error("Failure! File does not exist.")
    else:
        logger.error("Capture failed reported by recorder.")

if __name__ == "__main__":
    test_capture()
