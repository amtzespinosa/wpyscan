# theme_enum.py
import requests
from bs4 import BeautifulSoup
import re
from user_agents import get_random_user_agent

def extract_installed_themes(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        if response.status_code == 200 or response.status_code == 401 or response.status_code == 403 or response.status_code == 500:
            soup = BeautifulSoup(response.text, 'html.parser')
            stylesheet_links = soup.find_all('link', attrs={'rel': 'stylesheet'}) 
            installed_themes = []
            for link in stylesheet_links:
                href = link.get('href')
                if 'themes' in href:
                    theme_name = re.search(r'/themes/([^/]+)/', href)
                    if theme_name:
                        theme_info = {
                            'name': theme_name.group(1),
                            'url': href
                        }
                        installed_themes.append(theme_info)

            return installed_themes

    except requests.RequestException as e:
        print(f"[-] An error occurred: {e}")
        return None

def extract_version_css(installed_themes):
    if installed_themes:
        print(f"[+] Installed Themes:")
        theme_list = []
        for theme in installed_themes:
            if theme['name'] not in theme_list:
                theme_list.append(theme['name'])
                css_url = theme['url']
                version = css_url[-5:]
                match = re.search(r'/themes/(.*?)/', css_url)
                if match:
                    result = match.group(1)
                    print(f" |- {result} {version}")
                    print(f" |- {css_url}")
