# atom.py

import requests
import re

def extract_wordpress_version_atom(url):
    method = "Atom (Passive Detection)"
    try:
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            match = re.search(r'<generator>https://wordpress.org/\?v=(\d+\.\d+(\.\d+)?)</generator>', response.text)
            if match:
                version = match.group(1)
                return version, method
    except requests.RequestException:
        pass
    return None
