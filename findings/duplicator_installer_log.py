import re
import requests

class DuplicatorInstallerLog:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        path = 'installer-log.txt'
        body = self.head_and_get(path).text

        if self.duplicator_pattern_match(body):
            result = {
                'url': self.url + path,
                'confidence': 100,
                'found_by': 'DIRECT ACCESS'
            }
            return result

        return None

    def duplicator_pattern_match(self, body):
        return bool(re.search(r'DUPLICATOR(-|\s)?(PRO|LITE)?:? INSTALL-LOG', body, re.IGNORECASE))

    def head_and_get(self, path):
        try:
            response = requests.head(self.url + path, allow_redirects=False)
            if response.status_code == 200:
                response = requests.get(self.url + path)
                return response
            return response
        except requests.RequestException:
            return requests.Response()