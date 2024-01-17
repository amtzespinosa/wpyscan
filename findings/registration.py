# registration.py

import requests
from bs4 import BeautifulSoup

class Registration:
    def __init__(self, url):
        self.url = url

    def passive(self, _opts=None):
        # Placeholder: Check in the homepage if there is the registration URL
        homepage_content = self.get_page_content(self.url)
        if homepage_content and 'wp-login.php?action=register' in homepage_content:
            return {
                'url': self.url,
                'confidence': 100,
                'found_by': 'PASSIVE_DETECTION'
            }
        return None

    def aggressive(self, _opts=None):
        registration_url = self.get_registration_url()
        res = self.get_and_follow_location(registration_url)

        if not res or res.status_code != 200:
            return None

        forms = res.html.select('form#setupform') + res.html.select('form#registerform')
        if not forms:
            return None

        return {
            'url': res.url,
            'confidence': 100,
            'found_by': 'DIRECT_ACCESS'
        }

    def get_registration_url(self):
        homepage_content = self.get_page_content(self.url)
        if homepage_content:
            soup = BeautifulSoup(homepage_content, 'html.parser')
            registration_link = soup.find('a', {'href': 'wp-login.php?action=register'})
            return registration_link['href'] if registration_link else None
        return None

    def get_and_follow_location(self, url):
        try:
            return requests.get(url, allow_redirects=True)
        except requests.RequestException:
            return None

    def get_page_content(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            pass
        return None