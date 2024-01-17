# comments.py

import requests
import re
from avoidance.user_agents import get_random_user_agent

def extract_wordpress_version_meta(url):
    method = "Meta Generator (Passive Detection)"
    try:
        # response = requests.get(url)
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        # Extract version from Meta Generator tag
        meta_generator_match = re.search(r'<meta name="generator" content="WordPress ([0-9.]+)"', response.text)
        if meta_generator_match:
            version = meta_generator_match.group(1)
            return version, method
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

    return None, None
