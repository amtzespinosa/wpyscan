import requests
import re

class UploadSQLDump:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        path = 'wp-content/uploads/dump.sql'
        res = self.head_and_get_with_range(path, [200], headers={'Range': 'bytes=0-3000'})

        if self.sql_pattern_match(res.text):
            result = {
                'url': self.url + path,
                'confidence': 100,
                'found_by': 'DIRECT ACCESS'
            }
            return result

        return None

    def sql_pattern_match(self, body):
        sql_pattern = r'(?:DROP|CREATE|(?:UN)?LOCK) TABLE|INSERT INTO'
        return bool(re.search(sql_pattern, body))

    def head_and_get_with_range(self, path, expected_status, get=None, headers=None):
        try:
            response = requests.head(self.url + path, allow_redirects=False)
            if response.status_code in expected_status:
                if get:
                    response = requests.get(self.url + path, **get, headers=headers)
                    return response
            return response
        except requests.RequestException:
            return requests.Response()