import requests

class Multisite:
    def __init__(self, url):
        self.url = url

    def aggressive(self, _opts=None):
        result = {'url': self.url + 'wp-signup.php', 'confidence': 0, 'found_by': ''}

        response = requests.get(result['url'])
        location_header = response.headers.get('location', '')
        status_code = response.status_code

        if status_code in [200, 302]:
            if status_code == 302 and 'wp-login.php?action=register' in location_header:
                return None

            if status_code == 200 or (status_code == 302 and 'wp-signup.php' in location_header):
                result['confidence'] = 100
                result['found_by'] = 'DIRECT ACCESS'
                return result

        return None
