import requests
import re

class EmergencyPasswdReset:
    def __init__(self, target_url):
        self.target_url = target_url

    def aggressive(self):
        path = 'emergency.php'
        res = self.request_target(path)

        if res and res.status_code == 200 and not self.is_homepage_or_404(res):
            confidence = 100 if re.search(r'password', res.text, re.IGNORECASE) else 40
            print('URL: ' + self.target_url + path)
            print(f'Confidence: {confidence}')
            print('Found By: DIRECT ACCESS')

    def request_target(self, path):
        try:
            return requests.head(self.target_url + path, allow_redirects=True, timeout=5)
        except requests.RequestException:
            return None

    def is_homepage_or_404(self, response):
        return response.url.rstrip('/') == self.target_url.rstrip('/') or response.status_code == 404