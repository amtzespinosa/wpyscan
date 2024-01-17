import re

def extract_version_css(installed_themes):
    if installed_themes:
        print(f"[+] Installed Themes:")
        theme_list = []
        for theme in installed_themes:
            if theme['name'] not in theme_list:
                theme_list.append(theme['name'])
                css_url = theme['url']
                theme_name = re.search(r'/themes/(.*?)/', css_url)
                theme_version = re.search(r'ver=(\d+\.\d+(\.\d+)?)', css_url)
                
                if theme_version:
                    version = css_url[-5:]
                if theme_name and theme_version:
                    theme = theme_name.group(1)
                    print(f" |- {theme} {version}")
                    print(f" |- {css_url}")
                else:
                    theme = theme_name.group(1)
                    print(f" |- {theme}")
                    print(f" |- Unknown version.")
                    print(f" |- {css_url}")
