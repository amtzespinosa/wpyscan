import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

class ConfigBackup:
    def __init__(self, url):
        self.url = url

class KnownFilenames:
    def __init__(self, target):
        self.target = target

    def aggressive(self, opts=None):
        found = []

        for filename in self.get_potential_filenames():
            url = urljoin(self.target, filename)
            response = requests.get(url)
            
            if 200 <= response.status_code < 300 and re.search(r'define', response.text, re.I) and not re.search(r'<\s?html', response.text, re.I):
                found.append(ConfigBackup(url))

        return found

    def get_potential_filenames(self):
        # Replace with your own array of potential filenames
        return ['wp-config.php', 'config.php', 'settings.php']
