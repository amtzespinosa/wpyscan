import requests
import json
from avoidance.user_agents import get_random_user_agent

class OembedApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def aggressive(self):
        try:
            # response = requests.get(self.api_url)
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(self.api_url, headers=headers)
            oembed_data = json.loads(response.text)

            if oembed_data:
                self.print_user_details(oembed_data)
            else:
                print("[-] No user details found in the Oembed API response.")

        except (json.JSONDecodeError, requests.RequestException) as e:
            print(f"Error: {e}")

    def print_user_details(self, oembed_data):
        usernames = []
        if 'author_url' in oembed_data and '/author/' in oembed_data['author_url']:
            username = oembed_data['author_url'].split('/author/')[-1]
            username = username.rstrip('/')
        if 'author_name' in oembed_data and oembed_data['author_name']:
            name = oembed_data['author_name']
        user_dict = {username: name}
        for result in oembed_data:
            if user_dict not in usernames:
                usernames.append(user_dict)
                print(f"[+] Username: {username}")
                print(f" |- Author Name: {oembed_data['author_name']}")
            else:
                usernames.append(user_dict)
                if usernames.count(user_dict) == 2:
                    print(f" |- {username} confirmed by Post Author (Passive Detection)")
                else: pass

