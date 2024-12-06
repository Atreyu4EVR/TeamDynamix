import time
from functools import wraps
from collections import defaultdict
import threading

class RateLimiter:
    """Rate limiter for TeamDynamix API - configurable calls per IP address per period"""
    
    def __init__(self, max_calls: int = 60, period: int = 60):
        """
        Initialize rate limiter with configurable limits
        
        Args:
            max_calls: Maximum number of calls allowed per period (default: 60)
            period: Time period in seconds (default: 60)
        """
        self.max_calls = max_calls
        self.period = period
        self.timestamps = defaultdict(list)
        self.timestamps['api'] = []
        self.lock = threading.Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                now = time.time()
                
                # Clean old timestamps
                self.timestamps['api'] = [
                    ts for ts in self.timestamps['api'] 
                    if now - ts < self.period
                ]

                # Check if we've exceeded the rate limit
                if len(self.timestamps['api']) >= self.max_calls:
                    oldest_call = self.timestamps['api'][0]
                    sleep_time = self.period - (now - oldest_call)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                        now = time.time()

                # Add current timestamp
                self.timestamps['api'].append(now)
                
                return func(*args, **kwargs)
        return wrapper