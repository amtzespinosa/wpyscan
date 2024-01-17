import requests
import time
from user_agents import get_random_user_agent

class ProxyHandler:
    def __init__(self, proxy_api=None):
        self.proxy_api = proxy_api
        self.proxy_list = self.fetch_proxy_api()

    def fetch_proxy_api(self):
        try:
            response = requests.get(self.proxy_api)
            if response.status_code == 200:
                return [self.parse_proxy_line(line) for line in response.text.strip().split('\n') if line.strip()]
            else:
                print(f"Error fetching proxy information from API. Status code: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error fetching proxy information from API: {e}")
            return []

    def parse_proxy_line(self, line):
        host, port = line.split(':')
        return {"host": host, "port": int(port)}

    def get_requests_session(self, proxy):
        session = requests.Session()

        if proxy:
            session.proxies = {
                'http': f"http://{proxy['host']}:{proxy['port']}",
                'https': f"http://{proxy['host']}:{proxy['port']}",
            }
            session.verify = False  # You may want to remove this line if the proxy supports HTTPS

        return session

    def execute_request(self, url, method='get', headers=None, params=None, data=None):
        for proxy_info in self.proxy_list:
            print(f" |- Trying with proxy: {proxy_info['host']}:{proxy_info['port']}")
            session = self.get_requests_session(proxy_info)
            attempt = 1
            while attempt <= 3:
                try:
                    response = session.request(method, url, headers=headers, params=params, data=data)
                    return response

                except requests.RequestException as e:
                    print(f" |- Error: {e}")
                    attempt += 1
                    time.sleep(5)

        print("[-] Failed to obtain a successful response with any proxy.")
        return None
