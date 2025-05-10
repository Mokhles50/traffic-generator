from flask import Flask
import requests
import time
import random
import threading
from datetime import datetime

app = Flask(__name__)

# Store logs in memory
visit_logs = []
last_updated = datetime.now()

CONFIG = {
    "url": "https://example.com",  # CHANGE THIS
    "interval_min": 30,
    "interval_max": 120,
    "user_agents": [
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
    ]
}

def generate_traffic():
    global last_updated
    while True:
        try:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            response = requests.get(CONFIG['url'], headers=headers)
            
            log_entry = {
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': response.status_code,
                'url': CONFIG['url']
            }
            visit_logs.append(log_entry)
            last_updated = datetime.now()
            
            time.sleep(random.randint(CONFIG['interval_min'], CONFIG['interval_max']))
        except Exception as e:
            error_entry = {
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'error': str(e)
            }
            visit_logs.append(error_entry)
            time.sleep(60)

@app.route('/')
def home():
    logs_to_show = visit_logs[-10:]  # Show last 10 entries
    logs_html = "<br>".join([
        f"{log['time']} - Status: {log.get('status', '')} {log.get('error', '')}"
        for log in logs_to_show
    ])
    return f"""
    <h1>Traffic Generator Running</h1>
    <h3>Target URL: {CONFIG['url']}</h3>
    <p>Last updated: {last_updated.strftime("%Y-%m-%d %H:%M:%S")}</p>
    <div style='border:1px solid #ccc; padding:10px;'>
        {logs_html if logs_to_show else "No visits logged yet"}
    </div>
    """

if __name__ == '__main__':
    threading.Thread(target=generate_traffic, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
