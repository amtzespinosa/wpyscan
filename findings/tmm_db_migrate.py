import requests

class TmmDbMigrate:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        path = 'wp-content/uploads/tmm_db_migrate/tmm_db_migrate.zip'
        url = self.url + path
        res = self.head_or_get_request(url)

        if self.is_valid_response(res):
            result = {
                'url': url,
                'confidence': 100,
                'found_by': 'DIRECT ACCESS'
            }
            return result

        return None

    def head_or_get_request(self, url):
        try:
            response = requests.head(url, allow_redirects=False)
            if response.status_code == 200:
                response = requests.get(url)
            return response
        except requests.RequestException:
            return requests.Response()

    def is_valid_response(self, response):
        return response.status_code == 200 and response.headers['Content-Type'].lower().startswith('application/zip')
