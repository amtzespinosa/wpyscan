import requests

class UploadDirectoryListing:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        path = 'wp-content/uploads/'

        if self.directory_listing_enabled(path):
            result = {
                'url': self.url + path,
                'confidence': 100,
                'found_by': 'DIRECT ACCESS'
            }
            return result

        return None

    def directory_listing_enabled(self, path):
        try:
            response = requests.get(self.url + path)
            return response.status_code == 200 and 'Index of /' in response.text
        except requests.RequestException:
            return False