import requests

class WpCron:
    def __init__(self, url):
        self.url = url

    def check_wp_cron(self):
        try:
            wp_cron_url = f"{self.url.rstrip('/')}/wp-cron.php"
            response = requests.get(wp_cron_url)

            if 200 <= response.status_code < 300:
                return response.text
        except requests.RequestException:
            pass

        return None
