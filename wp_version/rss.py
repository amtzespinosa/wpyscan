# rss.py

import requests
import re
from avoidance.user_agents import get_random_user_agent

def extract_wordpress_version_rss(url):
    method = "RSS (Passive Detection)"
    feed_url = url.rstrip('/') + "/feed"
    try:
        # response = requests.get(feed_url)
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(feed_url, headers=headers, allow_redirects=True)

        if 200 <= response.status_code < 300:
            match = re.search(r'<generator>https://wordpress.org/\?v=(\d+\.\d+(\.\d+)?)</generator>', response.text)
            if match:
                version = match.group(1)
                return version, method
    except requests.RequestException:
        pass
    return None
