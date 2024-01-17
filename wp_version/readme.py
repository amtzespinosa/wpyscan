# readme.py

import re
import requests
from avoidance.user_agents import get_random_user_agent

def extract_wordpress_version_readme(url):
    method = "Readme (Passive Detection)"
    try:
        # response = requests.get(url)
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, allow_redirects=True)

        if 200 <= response.status_code < 300:
            match = re.search(r'Stable tag: (\d+\.\d+(\.\d+)?)', response.text)
            if match:
                version = match.group(1)
                return version, method
    except requests.RequestException:
        pass
    return None
