import asyncio
import logging
import time
from datetime import datetime
from recorder import BladeRFRecorder
from decoder import ADSBCoder
from utils import setup_logging

logger = logging.getLogger(__name__)

class ADSBEngine:
    def __init__(self, capture_file="/tmp/adsb_continuous.bin"):
        self.capture_file = capture_file
        self.recorder = BladeRFRecorder(file_path=self.capture_file)
        self.decoder = ADSBCoder(self.capture_file)
        self.aircraft_data = {}
        self.is_running = False
        self.last_seen = {}

    async def run_loop(self):
        self.is_running = True
        logger.info("ADS-B Engine loop started.")
        while self.is_running:
            try:
                loop = asyncio.get_event_loop()
                success = await loop.run_in_executor(None, self.recorder.start)
                if not success:
                    logger.error("Capture burst failed. Retrying in 5s...")
                    await asyncio.sleep(5)
                    continue
                new_aircraft = self.decoder.decode_file()
                now = datetime.now()
                for aircraft in new_aircraft:
                    hex_id = aircraft.get('icao', 'Unknown')
                    self.aircraft_data[hex_id] = {
                        **aircraft,
                        'last_updated': now.strftime("%H:%M:%S")
                    }
                    self.last_seen[hex_id] = time.time()
                current_time = time.time()
                stale_ids = [hid for hid, last in self.last_seen.items() if current_time - last > 120]
                for hid in stale_ids:
                    self.aircraft_data.pop(hid, None)
                    self.last_seen.pop(hid, None)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.exception(f"Error in engine loop: {e}")
                await asyncio.sleep(5)

    def stop(self):
        self.is_running = False
        logger.info("ADS-B Engine loop stopping.")

    def get_all_aircraft(self):
        return list(self.aircraft_data.values())

engine = ADSBEngine()
