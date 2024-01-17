import requests
from avoidance.user_agents import get_random_user_agent

class ThemesBruteForce:
    def __init__(self, target_url, theme_list_file):
        self.target_url = target_url
        self.theme_list_file = theme_list_file

    def enumerate_themes(self):
        theme_names_list = []
        try:
            with open(self.theme_list_file, 'r') as file:
                theme_names = file.read().splitlines()

            for theme_name in theme_names:
                theme_url = f"{self.target_url.rstrip('/')}/wp-content/themes/{theme_name}"
                # print(theme_url)
                # response = requests.get(theme_url)
                headers = {'User-Agent': get_random_user_agent()}
                response = requests.get(theme_url, headers=headers)
                if 200 <= response.status_code < 300 or response.status_code == 403:
                    # print(f"theme found: {theme_name} - URL: {theme_url}")
                    theme_names_list.append(theme_name)
                else:
                    theme_readme_url = f"{self.target_url.rstrip('/')}/wp-content/themes/{theme_name}/readme.txt"
                    # response = requests.get(theme_readme_url)
                    headers = {'User-Agent': get_random_user_agent()}
                    response = requests.get(theme_readme_url, headers=headers)
                    if 200 <= response.status_code < 300 or response.status_code == 403:
                        # print(f"theme found: {theme_name} - URL: {theme_readme_url}")
                        theme_names_list.append(theme_name)
            return theme_names_list        

        except FileNotFoundError:
            print(f"Error: theme list file not found - {self.theme_list_file}")
        except Exception as e:
            print(f"Error: {e}")
