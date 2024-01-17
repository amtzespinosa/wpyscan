# comments.py

import requests
import re

def extract_wordpress_version_comments(url):
    method = "Comments (Passive Detection)"
    try:
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            match = re.search(r'content=["\']WordPress (\d+\.\d+(\.\d+)?)', response.text)
            if match:
                version = match.group(1)
                return version, method
    except requests.RequestException:
        pass
    return None
