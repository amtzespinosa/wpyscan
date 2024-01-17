import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from avoidance.user_agents import get_random_user_agent

class Plugin:
    def __init__(self, slug, confidence):
        self.slug = slug
        self.confidence = confidence

class UrlsInHomepageFinder:
    def __init__(self, target_url):
        self.target_url = target_url

    def passive(self):
        found = []

        # Extract items from links and codes related to plugins, remove duplicates, and sort
        plugins = list(set(self.items_from_links('plugins') + self.items_from_codes('plugins')))
        plugins.sort()

        for slug in plugins:
            found.append(Plugin(slug, confidence=80))

        return found

    def items_from_links(self, path):
        links = self.extract_links_from_page()
        return [link for link in links if path in link]

    def items_from_codes(self, path):
        codes = self.extract_codes_from_page()
        return [code for code in codes if path in code]

    def extract_links_from_page(self):
        try:
            # response = requests.get(self.target_url)
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(self.target_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a', href=True)]
            return [urljoin(self.target_url, link) for link in links]
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def extract_codes_from_page(self):
        try:
            # response = requests.get(self.target_url)
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(self.target_url, headers=headers)
            response.raise_for_status()
            return response.text.split()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []