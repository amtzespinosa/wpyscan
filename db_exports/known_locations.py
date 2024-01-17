import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup  # Assuming you have BeautifulSoup installed
import requests

class DbExport:
    def __init__(self, url):
        self.url = url
        

class KnownLocations:
    def __init__(self, target, filename_list_file):
        self.target = target
        self.filename_list_file = filename_list_file

    def valid_response_codes(self):
        return [200, 206]

    def sql_pattern(self):
        return re.compile(r'(?:DROP|(?:UN)?LOCK|CREATE|ALTER) (?:TABLE|DATABASE)|INSERT INTO')

    def aggressive(self, opts=None):
        found = []

        for url, index in self.potential_urls(opts):
            res = requests.get(url, headers={'Range': 'bytes=0-3000'})

            if url.endswith('.zip'):
                if re.match(r'\Aapplication/zip', res.headers['Content-Type'], re.I):
                    found.append(DbExport(url))
            elif self.sql_pattern().search(res.text):
                found.append(DbExport(url))

        return found

    def full_request_params(self):
        return {'headers': {'Range': 'bytes=0-3000'}}

    def potential_urls(self, opts=None):
        urls = {}
        index = 0

        with open(self.filename_list_file, 'r') as file:
                possible_locations = file.read().splitlines()

        for path in possible_locations:
            path = path.strip()

            if '{domain_name}' in path:
                urls[urljoin(self.target, path.replace('{domain_name}', self.domain_name()))] = index

                if self.domain_name() != self.domain_name_with_sub():
                    urls[urljoin(self.target, path.replace('{domain_name}', self.domain_name_with_sub()))] = index + 1

                    index += 1
            else:
                urls[urljoin(self.target, path)] = index

            index += 1

        return urls.items()

    def domain_name(self):
        domain_name = self.target.split('//')[1].split('/')[0]
        return domain_name

    def domain_name_with_sub(self):
        return self.target.split('//')[1].split('/')[0]

    def create_progress_bar(self, opts=None):
        pass  # You can add a progress bar implementation if needed
