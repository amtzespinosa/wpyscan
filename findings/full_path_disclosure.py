# full_path_disclosure.py

import requests

class FullPathDisclosure:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        path = 'wp-includes/rss-functions.php'
        fpd_entries = self.full_path_disclosure_entries(path)

        if fpd_entries:
            return {
                'url': self.url + path,
                'confidence': 100,
                'found_by': 'DIRECT ACCESS',
                'interesting_entries': fpd_entries
            }

        return None

    def full_path_disclosure_entries(self, path):
        try:
            response = requests.get(self.url + path)

            if 200 <= response.status_code < 300:
                lines = response.text.splitlines()
                return [line.strip() for line in lines if line.strip()]

            return []

        except requests.RequestException:
            return []
