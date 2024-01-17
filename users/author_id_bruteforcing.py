import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from avoidance.user_agents import get_random_user_agent

class AuthorIdBruteForcing:
    def __init__(self, target):
        self.target = target

    def valid_response_codes(self):
        return [200, 301, 302]

    def aggressive(self, opts=None):
        found = []
        found_by_msg = 'Author Id Brute Forcing - %s (Aggressive Detection)'

        for res, _id in self.enumerate(self.target_urls(opts)):
            username, found_by, confidence = self.potential_username(res)

            if username:
                found.append({
                    'username': username,
                    'id': _id,
                    'found_by': found_by_msg % found_by,
                    'confidence': confidence
                })

        return found

    def target_urls(self, opts=None):
        if opts is None:
            opts = {}

        urls = {}

        for _id in opts.get('range', range(1, 300)):
            urls[urljoin(self.target, f"?author={_id}")] = _id

        return urls

    def enumerate(self, urls, opts=None):
        if opts is None:
            opts = {}

        for url, _id in urls.items():
            res = self.get_and_follow_location(url)

            if res.status_code in self.valid_response_codes():
                yield res, _id

    def get_and_follow_location(self, url):
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, allow_redirects=True)
        return DummyResponse(response.status_code, response.text, response.url)

    def potential_username(self, res):
        username = self.username_from_author_url(res.url) or self.username_from_response(res)

        if username:
            return username, 'Author Pattern', 100

        username = self.display_name_from_body(res.text)

        if username:
            return username, 'Display Name', 50

        return None, None, None

    def username_from_author_url(self, uri):
        uri = urljoin(self.target, uri)

        match = re.search(r'/author/([^/\b]+)/?', uri, re.IGNORECASE)
        return match.group(1) if match else None

    def username_from_response(self, res):
        # Permalink enabled
        for uri in self.in_scope_uris(res.text, '//@href[contains(., "author/")]'):
            username = self.username_from_author_url(uri)
            if username:
                return username

        # No permalink
        match = re.search(r'<body class="archive author author-([^\s]+)[ "]', res.text, re.IGNORECASE)
        return match.group(1) if match else None

    def display_name_from_body(self, body):
        page = BeautifulSoup(body, 'html.parser')

        # WP >= 3.0
        for node in page.select('h1.page-title span'):
            text = node.text.strip()
            if text:
                return text

        # WP < 3.0
        for node in page.find_all('link', rel='alternate', type='application/rss+xml'):
            title = node.get('title')

            match = re.search(r'Posts by (.*) Feed\z', title, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

class DummyResponse:
    def __init__(self, status_code=200, text="", url=""):
        self.status_code = status_code
        self.text = text
        self.url = url

