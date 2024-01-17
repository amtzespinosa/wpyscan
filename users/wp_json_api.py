import requests, json, time
from avoidance.user_agents import get_random_user_agent
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WPJsonApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def aggressive(self):
        try:
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(self.api_url, headers=headers)

            if 200 <= response.status_code < 300:
                if self.detect_captcha(response.text):
                    print(" |- Captcha or redirect detected. Handle accordingly.")
                else:
                    json_data = response.json()
                    if 'slug' in json_data and json_data['slug']:
                        self.print_user_details(json_data)
                    else:
                        print("[-] No user details found in the WordPress JSON API response.")

        except (json.JSONDecodeError, requests.RequestException) as e:
            pass

    def detect_captcha(self, response_text):
        return "Captcha" in response_text or "redirect" in response_text

    def print_user_details(self, json_data):
        usernames = []
        if 'slug' in json_data and json_data['slug']:
            username = json_data['slug']
        if 'name' in json_data and json_data['name']:
            name = json_data['name']
        user_dict = {username: name}
        for result in json_data:
            if user_dict not in usernames:
                usernames.append(user_dict)
                print(f"[+] Username: {username}")
                print(f" |- Author Name: {json_data['name']}")
            else:
                usernames.append(user_dict)

class WPJsonApiProxy:
    def __init__(self, api_url, proxy_api=None):
        self.api_url = api_url
        self.proxy_api = proxy_api
        self.proxy_list = self.fetch_proxy_api()

    def fetch_proxy_api(self):
        try:
            response = requests.get(self.proxy_api)
            if response.status_code == 200:
                return [self.parse_proxy_line(line) for line in response.text.strip().split('\n') if line.strip()]
            else:
                return []
        except requests.RequestException as e:
            return []

    def parse_proxy_line(self, line):
        host, port = line.split(':')
        return {"host": host, "port": int(port)}

    def get_requests_session(self, proxy):
        session = requests.Session()

        if proxy:
            session.proxies = {
                'http': f"socks5://{proxy['host']}:{proxy['port']}",
                'https': f"socks5://{proxy['host']}:{proxy['port']}",
            }
            session.verify = False  # You may want to remove this line if the proxy supports HTTPS

        return session

    def aggressive(self):
        max_retries = 3
        retry_delay = 5  # seconds
        max_polling_attempts = 10
        polling_interval = 5  # seconds

        for proxy_info in self.proxy_list:
            for attempt in range(1, max_retries + 1):
                try:
                    session = self.get_requests_session(proxy_info)
                    headers = {'User-Agent': get_random_user_agent()}
                    response = session.get(self.api_url, headers=headers)

                    if response.status_code == 202:
                        for _ in range(max_polling_attempts):
                            time.sleep(polling_interval)
                            response = session.get(self.api_url, headers=headers)
                            if response.status_code != 202:
                                break

                    if 200 <= response.status_code < 300:
                        if response.text.strip():
                            json_data = response.json()
                            if isinstance(json_data, list):
                                print("[+] Usernames found:")
                                for user_data in json_data:
                                    self.print_user_details(user_data)
                            else:
                                self.print_user_details(json_data)
                            return  # Exit the loop if successful

                except (json.JSONDecodeError, requests.RequestException) as e:
                    break

    def print_user_details(self, json_data):
        try:
            username = json_data.get('slug', '')
            name = json_data.get('name', '')

            if username:
                print(f" |- Author Name: {name}")
                print(f" |- Username: {username}")
                print("")
            else:
                print("[-] No username found in the WordPress JSON API response.")
        except Exception as e:
            print(f" |- Error parsing user details: {e}")
