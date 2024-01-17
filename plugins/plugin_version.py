import re, requests
from avoidance.user_agents import get_random_user_agent

class PluginVersionExtractor:
    DEFAULT_CONFIDENCE = 40

    def __init__(self, target_url, plugin_names):
        self.target_url = target_url
        self.plugin_names = plugin_names
        self.info = []

    def extract_versions(self):
        for plugin_name in self.plugin_names:
            # print(f"\nProcessing plugin: {plugin_name}")
            info = self.extract_info(plugin_name)
            if info:
                self.info.append({'url': plugin_name, 'name': info[1], 'version': info[0]})
        
    def extract_info(self, plugin_name):
        search_url = f"{self.target_url.rstrip('/')}/wp-content/plugins/{plugin_name}/readme.txt"
        try:
            # response = requests.get(search_url)
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(search_url, headers=headers)
            # Check if the readme file exists
            if response.status_code == 200:
                # print(f"Readme found for {plugin_name}")
                # Extract the plugin name from the readme content
                plugin_name_match = re.search(r'===\s*(.+?)\s*===', response.text)
                long_name = str(plugin_name_match)[43:-5]
                plugin_name = long_name.split("-")[0]
                # print(plugin_name)

                if plugin_name_match:
                    readme_plugin_name = plugin_name_match.group(1)
                    # print(f"Plugin name matched in the readme: {readme_plugin_name} (Expected: {plugin_name})")

                    # Extract the version using multiple patterns
                    version_patterns = [
                        r'Stable tag:\s*([0-9]+\.[0-9]+\.[0-9]+)',
                        r'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)'
                        # Add more patterns as needed
                    ]

                    for pattern in version_patterns:
                        version_match = re.search(pattern, response.text, re.IGNORECASE)
                        if version_match:
                            version = version_match.group(1)
                            # print(f"Version extracted: {version}")
                            return version, plugin_name

        except requests.exceptions.RequestException as e:
            print(f"Error searching for {plugin_name}: {e}")

        return None, None
