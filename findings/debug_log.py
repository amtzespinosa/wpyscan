import requests

class DebugLog:
    def __init__(self, url):
        self.url = url

    def aggressive(self):
        try:
            debug_log_url = f"{self.url.rstrip('/')}/wp-content/debug.log"
            response = requests.get(debug_log_url)

            if 200 <= response.status_code < 300:
                return debug_log_url

        except requests.RequestException as e:
            print(f"\n[-] An error occurred: {e}")