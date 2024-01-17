from datetime import datetime
import sys, argparse
from scanner import wp_version, headers, robots, xml_rpc, readme, wp_mu_plugins, \
    wp_cron, backup_db, debug_log, emergency_passwd_reset, full_path_disclosure, \
    registration, multisite, php_disabled, upload_directory_listing, upload_sql_dump, \
    duplicator_installer_log, tmm_db_migrate, known_filenames, known_locations, \
    author_id_bruteforcing, wp_json_api, author_post, author_sitemap, login_error_messages, \
    oembed_api, themes_source, themes_brute_force, theme_info, plugins_html, \
    plugins_homepage, plugins_version, plugins_brute_force \
    
from scanner import usernames
sys.dont_write_bytecode = True

if __name__ == "__main__":
    
    website_url = input("Enter a valid WordPress URL: ")



    print("""
 _  _  ________        ______                   
(_||_||_______ \\      / _____)                  
 _  _  _ _____) )   _( (____   ____ _____ ____  
| || || |  ____/ | | |\\____ \\ / ___|____ |  _ \\ 
| || || | |    | |_| |_____) | (___/ ___ | | | |
 \\_____/|_|     \\__  (______/ \\____)_____|_| |_|
               (____/ by @amtzespinosa - v1.0.0   
                  
""")

    print(f"[+] Scanning:       {website_url}")
    print(f"[+] Time started:   {str(datetime.now())}\n")

    print(" INTERESTING FINDINGS")
    print("+" + "-" * 50)

    # TODO: Filter functionality with sys.argv
    headers(website_url)
    robots(website_url)
    xml_rpc(website_url)
    readme(website_url)
    wp_mu_plugins(website_url)
    wp_cron(website_url)
    backup_db(website_url)
    debug_log(website_url)
    emergency_passwd_reset(website_url)
    full_path_disclosure(website_url)
    registration(website_url)
    multisite(website_url)
    php_disabled(website_url)
    upload_directory_listing(website_url)
    upload_sql_dump(website_url)
    duplicator_installer_log(website_url)
    tmm_db_migrate(website_url)

    known_filenames(website_url)
    known_locations(website_url)

    wp_version(website_url)

    print(" USERS ENUMERATION")
    print("+" + "-" * 50)

    # author_id_bruteforcing(website_url)
    # author_post(website_url)
    # author_sitemap(website_url)
    # login_error_messages(website_url)
    # oembed_api(website_url)
    # wp_json_api(website_url)

    def run_user_enumeration(website_url):
        functions_to_run = [
            wp_json_api,
            oembed_api,
            author_id_bruteforcing,
            author_post,
            author_sitemap,
            login_error_messages
        ]
        for func in functions_to_run:
            if func(website_url) is True:
                break

    run_user_enumeration(website_url)
    
    print("\n THEMES ENUMERATION")
    print("+" + "-" * 50)

    themes_source(website_url)
    themes_brute_force(website_url)
    theme_info(website_url)

    print("\n PLUGINS ENUMERATION")
    print("+" + "-" * 50)

    plugins_html(website_url)
    plugins_brute_force(website_url)
    plugins_version(website_url)

    # print("[+] Other Interesting Findings")
    # Use this to load data from which extract plugins info
    # plugins_homepage(website_url)
        
