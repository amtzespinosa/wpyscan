import requests

class Readme:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        for path in self.potential_files():
            res = self.head_and_get_request(path)

            if res.status_code == 200 and 'wordpress' in res.text.lower():
                result = {
                    'url': self.url + path,
                    'confidence': 100,
                    'found_by': 'DIRECT ACCESS'
                }
                return result

        return None

    def head_and_get_request(self, path):
        try:
            response = requests.head(self.url + path, allow_redirects=False)
            if response.status_code == 200:
                response = requests.get(self.url + path)
            return response
        except requests.RequestException:
            return requests.Response()

    def potential_files(self):
        return ['readme.html', 'olvasdel.html', 'lisenssi.html', 'liesmich.html']