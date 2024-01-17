import requests

class BackupDB:
    def __init__(self, target_url):
        self.target_url = target_url

    def aggressive(self):
        path = 'wp-content/backup-db/'
        res = self.request_target(path)

        if res and res.status_code in [200, 403] and not self.is_homepage_or_404(res):
            print('URL: ' + self.target_url + path)
            print('Confidence: 70%')
            print('Found By: DIRECT ACCESS')
            print('Interesting Entries:')
            entries = self.get_directory_listing_entries(path)
            if entries:
                for entry in entries:
                    print(entry)

    def request_target(self, path):
        try:
            return requests.head(self.target_url + path, allow_redirects=True, timeout=5)
        except requests.RequestException:
            return None

    def is_homepage_or_404(self, response):
        return response.url.rstrip('/') == self.target_url.rstrip('/') or response.status_code == 404

    def get_directory_listing_entries(self, path):
        try:
            res = requests.get(self.target_url + path, timeout=5)
            if res.status_code == 200:
                return res.text.splitlines()
        except requests.RequestException:
            pass
        return []