from flask import Flask
import requests
import time
import random
import threading
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configuration
CONFIG = {
    "url": "https://example.com",  # CHANGE THIS TO YOUR WEBSITE
    "interval_min": 10,           # Minimum seconds between visits
    "interval_max": 60,           # Maximum seconds between visits
    "duration": 1440,             # How many minutes to run (1440 = 24 hours)
    "user_agents": [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)...'
    ]
}

def generate_traffic():
    end_time = time.time() + CONFIG['duration'] * 60
    while time.time() < end_time:
        try:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            response = requests.get(CONFIG['url'], headers=headers, timeout=10)
            print(f"Visited {CONFIG['url']} - Status: {response.status_code}")
            
            # Random delay before next visit
            time.sleep(random.randint(CONFIG['interval_min'], CONFIG['interval_max']))
            
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(30)

@app.route('/')
def home():
    return "Traffic Generator is running"

def run_traffic():
    traffic_thread = threading.Thread(target=generate_traffic)
    traffic_thread.daemon = True
    traffic_thread.start()

if __name__ == '__main__':
    run_traffic()
    app.run(host='0.0.0.0', port=10000)
