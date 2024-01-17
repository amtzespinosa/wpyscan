import requests

class PHPDisabled:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        path = 'wp-includes/version.php'
        response = requests.get(self.url + path)

        if "$wp_version =" in response.text:
            return {
                'url': self.url + path,
                'confidence': 100,
                'found_by': 'DIRECT ACCESS'
            }

        return None
