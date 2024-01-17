import requests
from avoidance.user_agents import get_random_user_agent

class PluginsBruteForce:
    def __init__(self, target_url, plugin_list_file):
        self.target_url = target_url
        self.plugin_list_file = plugin_list_file

    def enumerate_plugins(self):
        plugin_names_list = []
        try:
            with open(self.plugin_list_file, 'r') as file:
                plugin_names = file.read().splitlines()

            for plugin_name in plugin_names:
                plugin_url = f"{self.target_url.rstrip('/')}/wp-content/plugins/{plugin_name}"
                # print(plugin_url)
                # response = requests.get(plugin_url)
                headers = {'User-Agent': get_random_user_agent()}
                response = requests.get(plugin_url, headers=headers)
                if 200 <= response.status_code < 300 or response.status_code == 403:
                    # print(f"Plugin found: {plugin_name} - URL: {plugin_url}")
                    plugin_names_list.append(plugin_name)
                else:
                    plugin_readme_url = f"{self.target_url.rstrip('/')}/wp-content/plugins/{plugin_name}/readme.txt"
                    # response = requests.get(plugin_readme_url)
                    headers = {'User-Agent': get_random_user_agent()}
                    response = requests.get(plugin_readme_url, headers=headers)
                    if 200 <= response.status_code < 300 or response.status_code == 403:
                        # print(f"Plugin found: {plugin_name} - URL: {plugin_readme_url}")
                        plugin_names_list.append(plugin_name)
            return plugin_names_list        

        except FileNotFoundError:
            print(f"Error: Plugin list file not found - {self.plugin_list_file}")
        except Exception as e:
            print(f"Error: {e}")
