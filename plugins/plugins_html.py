# plugins.py

import re
import requests
from bs4 import BeautifulSoup
from avoidance.user_agents import get_random_user_agent

def extract_plugins_from_html(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return extract_plugins_from_soup(soup)
    except requests.RequestException as e:
        print(f"[-] An error occurred: {e}")
    return []

def extract_plugins_from_soup(soup):
    plugins = set()
    
    # Extract plugins from script tags
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        script_content = script_tag.get_text()
        plugin_matches = re.findall(r'/wp-content/plugins/([^/]+)/', script_content)
        plugins.update(plugin_matches)
    
    # Extract plugins from CSS files
    css_links = soup.find_all('link', attrs={'rel': 'stylesheet'})
    for css_link in css_links:
        css_url = css_link.get('href')
        if css_url and 'plugins' in css_url:
            plugin_matches = re.findall(r'/wp-content/plugins/([^/]+)/', css_url)
            plugins.update(plugin_matches)
    
    return list(plugins)
