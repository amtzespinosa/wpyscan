import requests
import re

def extract_wordpress_version_from_source(url):
    method = "Source Code (Passive Detection)"
    try:
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            # Modify the regex pattern based on the structure of your HTML source
            match = re.search(r'/wp-includes/css/dist/block-library/style.min.css?ver=([0-9]+\.[0-9]+\.[0-9]+)', response.text)
            if match:
                version = match.group(1)
                print(version)
                return version, method
    except requests.RequestException:
        pass
    return None
