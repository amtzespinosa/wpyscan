import requests

class Robots:
    def __init__(self, url):
        self.url = url

    def check_robots_txt(self):
        try:
            robots_url = f"{self.url.rstrip('/')}/robots.txt"
            response = requests.get(robots_url)

            if 200 <= response.status_code < 300:
                return robots_url
            else:
                return f"[-] robots.txt not found. Status Code: {response.status_code}"

        except requests.RequestException as e:
            return f"[-] An error occurred: {e}"
