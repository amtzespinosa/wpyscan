import requests

class WpMuPlugins:
    def __init__(self, url):
        self.url = url

    def check_wp_mu_plugins(self):
        try:
            mu_plugins_url = f"{self.url.rstrip('/')}/wp-content/mu-plugins/"
            response = requests.get(mu_plugins_url)

            if 200 <= response.status_code < 300:
                return response.text
        except requests.RequestException:
            pass

        return None