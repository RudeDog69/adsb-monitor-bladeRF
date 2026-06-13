import sys
import logging
from recorder import BladeRFRecorder
from decoder import ADSBCoder
from utils import setup_logging

def main():
    setup_logging()
    logger = logging.getLogger("Main")
    
    capture_file = "/tmp/adsb_test.bin"
    recorder = BladeRFRecorder(frequency=109000000, samplerate=2000000, file_path=capture_file)
    decoder = ADSBCoder(capture_file)
    
    logger.info("Starting ADS-B Monitor...")
    
    if recorder.start():
        messages = decoder.decode_file()
        if messages:
            logger.info(f"Found {len(messages)} messages:")
            for msg in messages:
                logger.info(f"Decoded Message: {msg}")
        else:
            logger.warning("No messages decoded.")
    else:
        logger.error("Failed to capture data.")

if __name__ == "__main__":
    main()
