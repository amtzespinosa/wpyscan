import requests
from bs4 import BeautifulSoup
from models.author_sitemap import UserSitemap
from avoidance.user_agents import get_random_user_agent

class AuthorSitemap:
    def __init__(self, target):
        self.target = target

    def aggressive(self):
        found_by_msg = 'Author Sitemap - %s (Aggressive Detection)'
        found = []

        sitemap_url = self.sitemap_url()

        if sitemap_url:
            response = self.target_get(sitemap_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                for user_tag in soup.find_all('loc'):
                    username = self.extract_username(user_tag.text)

                    if username and not username.strip().isspace():
                        user = UserSitemap(username,
                                    found_by=found_by_msg % 'Author Pattern',
                                    confidence=100,
                                    interesting_entries=[sitemap_url])
                        found.append(user)

        return found

    def sitemap_url(self):
        return self.target.url('wp-sitemap-users-1.xml')

    def target_get(self, url):
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        return response

    def extract_username(self, url):
        return url.split('/')[-2]
