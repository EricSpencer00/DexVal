import logging
import time
from pydexcom import Dexcom, GlucoseReading
from DexcomAPI.defs import getDexcomConnection

class GlucoseDataCache:
    def __init__(self, dexcom, cache_duration=60, max_retries=3, retry_delay=5):
        """
        Initialize the cache with Dexcom connection and parameters for caching, retries, and delays.
        """
        self.dexcom = dexcom
        self.cache_duration = cache_duration  # Cache duration in seconds
        self.max_retries = max_retries        # Number of retries in case of failure
        self.retry_delay = retry_delay        # Delay between retries in seconds
        self._cache = None
        self._last_fetched = 0

    def _is_cache_valid(self):
        """
        Check if the cache is still valid based on cache_duration.
        """
        return time.time() - self._last_fetched < self.cache_duration

    def _fetch_glucose_readings(self, minutes, max_count):
        """
        Attempt to fetch glucose readings with retries.
        """
        for attempt in range(self.max_retries):
            try:
                logging.debug(f"Fetching glucose data (attempt {attempt + 1})...")
                return self.dexcom.get_glucose_readings(minutes=minutes, max_count=max_count)
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(self.retry_delay)
        logging.error("Max retries exceeded.")
        return None

    def get_glucose_readings(self, minutes=1440, max_count=288):
        """
        Retrieve glucose readings, using cache if valid.
        """
        if self._is_cache_valid() and self._cache:
            logging.debug("Returning cached glucose data.")
            return self._cache

        self._cache = self._fetch_glucose_readings(minutes, max_count)
        if self._cache:
            self._last_fetched = time.time()
        return self._cache

def main():
    # Setup Dexcom connection
    dexcom = getDexcomConnection()

    # Initialize GlucoseDataCache
    glucose_cache = GlucoseDataCache(dexcom)

    # Example: Get glucose readings from cache or fetch new if cache is expired
    glucose_readings = glucose_cache.get_glucose_readings()

    if glucose_readings:
        for reading in glucose_readings:
            print(f"Time: {reading.time}, Value: {reading.value}")
    else:
        print("Failed to retrieve glucose readings.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Enable debug logging
    main()
