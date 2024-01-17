import sys, os
sys.dont_write_bytecode = True

from wp_version.meta import extract_wordpress_version_meta
from wp_version.source_code import extract_wordpress_version_from_source
from wp_version.readme import extract_wordpress_version_readme
from wp_version.rss import extract_wordpress_version_rss

from findings.headers import Headers
from findings.robots import Robots
from findings.xml_rpc import XML_RPC
from findings.readme import Readme
from findings.mu_plugins import WpMuPlugins
from findings.wp_cron import WpCron
from findings.backup_db import BackupDB
from findings.debug_log import DebugLog
from findings.emergency_passwd_reset import EmergencyPasswdReset
from findings.full_path_disclosure import FullPathDisclosure
from findings.registration import Registration
from findings.multisite import Multisite
from findings.php_disabled import PHPDisabled
from findings.upload_directory_listing import UploadDirectoryListing
from findings.upload_sql_dump import UploadSQLDump
from findings.duplicator_installer_log import DuplicatorInstallerLog
from findings.tmm_db_migrate import TmmDbMigrate
from config_backups.known_filenames import KnownFilenames
from db_exports.known_locations import KnownLocations

from users.author_id_bruteforcing import AuthorIdBruteForcing
from users.author_posts import AuthorPosts
from models.author_posts import TargetPosts
from users.author_sitemap import AuthorSitemap
from models.author_sitemap import TargetSitemap
from users.loggin_error_massages import TargetLogin, LoginErrorMessages
from users.oembed_api import OembedApi
from users.wp_json_api import WPJsonApi, WPJsonApiProxy

from themes.found_themes import found_themes
from themes.themes_source import extract_installed_themes
from themes.theme_version_css import extract_version_css
from themes.theme_info_readme import ThemeVersionExtractor
from themes.brute_force_themes import ThemesBruteForce

from plugins.found_plugins import found_plugins
from plugins.plugins_html import extract_plugins_from_html
from plugins.brute_force_plugins import PluginsBruteForce
from plugins.urls_in_homepage import UrlsInHomepageFinder
from plugins.plugin_version import PluginVersionExtractor

from vulnerabilities.wordpress import check_wordpress_vulnerabilities
from vulnerabilities.theme import check_theme_vulnerabilities
from vulnerabilities.plugins import check_plugin_vulnerabilities

def wp_version(website_url):
    wordpress_version = None
    extraction_method_used = None
    # Confirm the version with different methods
    confirmation_method_used = None

    # Try different extraction methods
    result = extract_wordpress_version_meta(website_url)
    if result is not None and extraction_method_used is None:
        wordpress_version, extraction_method_used = result
    result = extract_wordpress_version_from_source(website_url)
    if result is not None and extraction_method_used is None:
        wordpress_version, extraction_method_used = result
    result = extract_wordpress_version_readme(website_url)
    if result is not None and extraction_method_used is None:
        wordpress_version, extraction_method_used = result
    result = extract_wordpress_version_rss(website_url)
    if result is not None and extraction_method_used is None:
        wordpress_version, extraction_method_used = result
    result = extract_wordpress_version_from_source(website_url)
 
    if extraction_method_used != "Source Code (Passive Detection)":      
        if result is not None and extraction_method_used != confirmation_method_used:
            version_confirmation, confirmation_method_used = result
    result = extract_wordpress_version_readme(website_url)
    if extraction_method_used != "Readme (Passive Detection)":       
        if result is not None and extraction_method_used != confirmation_method_used:
            version_confirmation, confirmation_method_used = result
    result = extract_wordpress_version_rss(website_url)
    if extraction_method_used != "RSS (Passive Detection)":        
        if result is not None and extraction_method_used != confirmation_method_used:
            version_confirmation, confirmation_method_used = result
    result = extract_wordpress_version_meta(website_url)
    if extraction_method_used != "Meta Generator (Passive Detection)":       
        if result is not None and extraction_method_used != confirmation_method_used:
            version_confirmation, confirmation_method_used = result

    if wordpress_version is not None:
        if confirmation_method_used is not None:
            if wordpress_version == version_confirmation:
                print(f"[+] WordPress version {wordpress_version} identified.")
                print(f" |- Found By: {extraction_method_used}")
                print(f" |- Version {version_confirmation} confirmed by {confirmation_method_used}")
                print("")
                check_wordpress_vulnerabilities(wordpress_version)
            else:
                print(f"[-] Version confirmation failed. Extracted version: {wordpress_version}")
        else:
            print(f"[+] WordPress version {wordpress_version} identified.")
            print(f" |- Found By: {extraction_method_used}")
            print("[-] Version not confirmed.")
    else:
        print("[-] WordPress version not identified.")

#################################################################################################

# Extract website's interesting info.
def headers(website_url):
    headers_analyzer = Headers(website_url)
    headers_result = headers_analyzer.analyze_headers()
    print(headers_result)
    print("")

def robots(website_url):
    robots_checker = Robots(website_url)
    robots_result = robots_checker.check_robots_txt()
    if robots_result:
        print(f"[+] robots.txt found: {robots_result}")
        print(" |- Found By: Robots Txt (Aggressive Detection)")
        print(" |- Confidence: 100%")
        print("")

def xml_rpc(website_url):
    xmlrpc_checker = XML_RPC(website_url)
    xmlrpc_result = xmlrpc_checker.check_xml_rpc()
    if xmlrpc_result:
        print(f"[+] XML-RPC seems to be enabled: {website_url.rstrip('/')}/xmlrpc.php")
        for reference in xmlrpc_checker.get_references():
            print(f" |- {reference}")
        print("")

def readme(website_url):
    readme_checker = Readme(website_url)
    readme_result = readme_checker.aggressive()
    if readme_result:
        print(f"[+] Readme found: {readme_result['url']}")
        print(f" |- Confidence: {readme_result['confidence']}%")
        print(f" |- Found By: {readme_result['found_by']}")
        print("")

def wp_mu_plugins(website_url):
    wp_mu_plugins_checker = WpMuPlugins(website_url)
    wp_mu_plugins_result = wp_mu_plugins_checker.check_wp_mu_plugins()
    if wp_mu_plugins_result:
        print(f"[+] This site has 'Must Use Plugins': {website_url.rstrip('/')}/wp-content/mu-plugins/")
        print("")

def wp_cron(website_url):
    wp_cron_checker = WpCron(website_url)
    wp_cron_result = wp_cron_checker.check_wp_cron()
    if wp_cron_result:
        print(f"[+] The external WP-Cron seems to be enabled: {website_url.rstrip('/')}/wp-cron.php")
        print("")

def backup_db(website_url):
    backup_db = BackupDB(website_url).aggressive()
    if backup_db:
        print("[+] Backup DB:")
        print(backup_db)
        print("")

def debug_log(website_url):
    debug_log = DebugLog(website_url).aggressive()
    if debug_log:
        print(f"[+] debug.log found: {debug_log}")
        print(f" |- Found By: debug.log (Aggressive Detection)")
        print(" |- Confidence: 100%")
        print("")

def emergency_passwd_reset(website_url):
    emergency_pwd_reset = EmergencyPasswdReset(website_url)
    pwd_reset = emergency_pwd_reset.aggressive()
    if pwd_reset:
        print("[+] Emergency Password Reset:")
        print(pwd_reset)
        print("")

def full_path_disclosure(website_url):
    full_path_disclosure_check = FullPathDisclosure(website_url)
    full_path_disclosure = full_path_disclosure_check.aggressive()
    if full_path_disclosure:
        print("[+] Full Path Disclosure:")
        print(f" |- URL: {full_path_disclosure['url']}")
        print(f" |- Confidence: {full_path_disclosure['confidence']}%")
        print(f" |- Found By: {full_path_disclosure['found_by']}")
        print(" |- Interesting Entries:")
        for entry in full_path_disclosure['interesting_entries']:
            print("     " + entry)
        print("")

def registration(website_url):
    registration_check = Registration(website_url)
    passive_result = registration_check.passive()
    aggressive_result = registration_check.aggressive()
    if passive_result or aggressive_result:
        print("[+] Registration ")
        if passive_result:
            print(" |- Registration found (Passive Detection):")
            print(passive_result)
        if aggressive_result:
            print(" |- Registration found (Aggressive Detection):")
            print(aggressive_result)
        print("")

def multisite(website_url):
    multisite_checker = Multisite(website_url)
    multisite_result = multisite_checker.aggressive()
    if multisite_result:
        print(f"[+] Registration link found: {multisite_result['url']}")
        print(f" |- Confidence: {multisite_result['confidence']}%")
        print(f" |- Found By: {multisite_result['found_by']}")
        print("")

def php_disabled(website_url):
    php_disabled_checker = PHPDisabled(website_url)
    php_disabled_result = php_disabled_checker.aggressive()
    if php_disabled_result:
        print(f"[+] PHP Disabled: {php_disabled_result['url']}")
        print(f" |- Confidence: {php_disabled_result['confidence']}%")
        print(f" |- Found By: {php_disabled_result['found_by']}")
        print("")

def upload_directory_listing(website_url):
    upload_listing_checker = UploadDirectoryListing(website_url)
    upload_listing_result = upload_listing_checker.aggressive()
    if upload_listing_result:
        print("[+] Upload Directory Listing:")
        print(f" |- URL: {upload_listing_result['url']}")
        print(f" |- Confidence: {upload_listing_result['confidence']}%")
        print(f" |- Found By: {upload_listing_result['found_by']}")
        print("")

def upload_sql_dump(website_url):
    upload_sql_dump_checker = UploadSQLDump(website_url)
    upload_sql_dump_result = upload_sql_dump_checker.aggressive()
    if upload_sql_dump_result:
        print("[+] Upload SQL Dump:")
        print(f" |- URL: {upload_sql_dump_result['url']}")
        print(f" |- Confidence: {upload_sql_dump_result['confidence']}%")
        print(f" |- Found By: {upload_sql_dump_result['found_by']}")
        print("")

def duplicator_installer_log(website_url):
    duplicator_installer_log_checker = DuplicatorInstallerLog(website_url)
    duplicator_installer_log_result = duplicator_installer_log_checker.aggressive()
    if duplicator_installer_log_result:
        print("[+] Duplicator Installer Log:")
        print(f" |- URL: {duplicator_installer_log_result['url']}")
        print(f" |- Confidence: {duplicator_installer_log_result['confidence']}%")
        print(f" |- Found By: {duplicator_installer_log_result['found_by']}")
        print("")

def tmm_db_migrate(website_url):
    tmm_db_migrate_checker = TmmDbMigrate(website_url)
    tmm_db_migrate_result = tmm_db_migrate_checker.aggressive()
    if tmm_db_migrate_result:
        print("[+] Tmm DB Migrate:")
        print(f" |- URL: {tmm_db_migrate_result['url']}")
        print(f" |- Confidence: {tmm_db_migrate_result['confidence']}%")
        print(f" |- Found By: {tmm_db_migrate_result['found_by']}")
        print("")

def known_filenames(website_url):
    known_filenames_checker = KnownFilenames(website_url)
    known_filenames_result = known_filenames_checker.aggressive()
    if known_filenames_result:
        print("[+] Config Backups Found:")
        for config_backup in known_filenames_result:
            print(f" |- {config_backup.url}")
        print("")

def known_locations(website_url):
    filename_list_file = "/usr/lib/wpyscan/db_exports/possible_locations.txt"  # Replace with the path to your theme list file
    known_locations_checker = KnownLocations(website_url, filename_list_file)
    known_locations_result = known_locations_checker.aggressive()
    if known_locations_result:
        print("[+] DB Exports Found:")
        for db_export in known_locations_result:
            print(f" - {db_export.url}")
        print("")

###########################################################################################
        
# Extract usernames via different methods
usernames = []

def author_id_bruteforcing(website_url):
    try:
        author_id_brute_forcing = AuthorIdBruteForcing(website_url)
        results = author_id_brute_forcing.aggressive({'range': range(1, 10)})
        for result in results:
            if result['username'] not in usernames:
                usernames.append(result['username'])
                print(f"[+] Username found: {result['username']}")
                print(f" |- User ID: {result['id']}")
                print(f" |- Found By: {result['found_by']}")
                print(f" |- Confidence: {result['confidence']}%")
                return True
    except: pass

def author_post(website_url):
    try:
        target = TargetPosts(website_url)
        author_posts_finder = AuthorPosts(target)
        results = author_posts_finder.passive()
        for result in results:
            if result[0] not in usernames:
                usernames.append(result[0])
                print(f"[+] Username found: {result[0]}")
                print(f" |- Found By: {result[1]}")
                print(f" |- Confidence: {result[2]}%")
                return True
            else:
                usernames.append(result[0])
                if usernames.count(result[0]) == 2:
                    print(f"{result[0]} confirmed by Post Author (Passive Detection)")
                else: pass
    except: pass

def author_sitemap(website_url):
    try:
        target = TargetSitemap(website_url)
        author_sitemap_finder = AuthorSitemap(target)
        results = author_sitemap_finder.aggressive()
        for user in results:
            print(f"Username: {user.username}, Found by: {user.found_by}, Confidence: {user.confidence}")
            return True
    except: pass

def login_error_messages(website_url):
    try:
        target = TargetLogin(website_url)
        login_error_messages_finder = LoginErrorMessages(target)
        results = login_error_messages_finder.aggressive()
        for user in results:
            print(f"Username: {user.username}, Found by: {user.found_by}, Confidence: {user.confidence}")
            return True
    except: pass

def oembed_api(website_url):
    try:
        api_url = f"{website_url.rstrip('/')}/wp-json/oembed/1.0/embed?url={website_url.rstrip('/')}&format=json"
        oembed_api_finder = OembedApi(api_url)
        oembed_api_finder.aggressive()
        return True
    except: pass

def wp_json_api(website_url):
    try:
        api_url = f"{website_url.rstrip('/')}/wp-json/wp/v2/users"
        wp_jason_api = WPJsonApi(api_url)
        response = wp_jason_api.aggressive()
        if response is None:
            # print(f" |- Workaround URL failed, search manually: {website_url.rstrip('/')}/?rest_route=/wp/v2/users")
            api_url = f"{website_url.rstrip('/')}/wp-json/wp/v2/users"
            proxy_api = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=yes&anonymity=elite'
            wp_api = WPJsonApiProxy(api_url, proxy_api=proxy_api)
            wp_api.aggressive()
            return True
    except:pass

##################################################################################################

# Extract installed themes
def themes_source(website_url):
    installed_themes = extract_installed_themes(website_url)
    for theme in installed_themes:
        name = theme['name']
        if name not in found_themes:
            found_themes.append(name.lower())
    return installed_themes
    # extract_version_css(installed_themes)
    
def themes_brute_force(website_url):
    theme_list_file = "/usr/lib/wpyscan/themes/top_themes.txt"  # Replace with the path to your theme list file
    theme_enumerator = ThemesBruteForce(website_url, theme_list_file)   
    theme_names_list = theme_enumerator.enumerate_themes()
    if theme_names_list:
        # print("[+] themes Identified:")
        for theme in theme_names_list:
            # print(f" |- {theme}")
            if theme not in found_themes:
                found_themes.append(theme)

def theme_info(website_url):
    theme_info_extractor = ThemeVersionExtractor(website_url, found_themes)
    theme_info_extractor.extract_versions()
    if found_themes:
        for data in theme_info_extractor.info:
            if 'version' in data and data['version'] is not None:
                print(f"   [+] {data['name']}")
                print(f"    |- Version: {data['version']} detected via Readme")
                print(f"    |- Found By: Readme (Aggressive Detection)")
                print(f"    |- Theme readme.txt: {website_url.rstrip('/')}/wp-content/themes/{data['url']}/readme.txt")
                print(f"    |- Theme location: {website_url.rstrip('/')}/wp-content/themes/{data['url']}")
                check_theme_vulnerabilities(data['url'], data['version'])
                print("")
            elif data['version'] is not None:
                print(f"{data['name']} - Version not found")
        if data['version'] == None:
            installed_themes = themes_source(website_url)
            extract_version_css(installed_themes)
            check_theme_vulnerabilities(data['url'], data['version'])
            print("")

#################################################################################################

def plugins_html(website_url):
    plugins = extract_plugins_from_html(website_url)
    if plugins:
        # print("[+] Plugins Identified:")
        for plugin in plugins:
            # print(f" |- {plugin}")
            found_plugins.append(plugin)
    else:
        print("[-] Failed to retrieve installed plugins via Passive Methods.")

def plugins_brute_force(website_url):
    plugin_list_file = "/usr/lib/wpyscan/plugins/top_plugins.txt"  # Replace with the path to your plugin list file
    plugin_enumerator = PluginsBruteForce(website_url, plugin_list_file)   
    plugin_names_list = plugin_enumerator.enumerate_plugins()
    if plugin_names_list:
        # print("[+] Plugins Identified:")
        for plugin in plugin_names_list:
            # print(f" |- {plugin}")
            if plugin not in found_plugins:
                found_plugins.append(plugin)

def plugins_homepage(website_url):
    finder = UrlsInHomepageFinder(website_url)
    plugins = finder.passive()
    if plugins:
        print(" |- [+] Files related to plugins:")
        for plugin in plugins:
            print(f" - {plugin.slug} (confidence: {plugin.confidence})")
    print("")

def plugins_version(website_url):
    plugin_version_extractor = PluginVersionExtractor(website_url, found_plugins)
    plugin_version_extractor.extract_versions()
    if found_plugins:
        print(f"[+] Plugins Detected")
        for data in plugin_version_extractor.info:
            if 'version' in data and data['version'] is not None:
                print(f"   [+] {data['name']}")
                print(f"    |- Version: {data['version']} detected via Readme")
                print(f"    |- Found By: Readme (Aggressive Detection)")
                print(f"    |- Plugin readme.txt: {website_url.rstrip('/')}/wp-content/plugins/{data['url']}/readme.txt")
                print(f"    |- Plugin location: {website_url.rstrip('/')}/wp-content/plugins/{data['url']}")
                print("")
                check_plugin_vulnerabilities(data['url'], data['version'])
                print("")
            elif data['version'] is not None:
                print(f"{data['name']} - Version not found")
