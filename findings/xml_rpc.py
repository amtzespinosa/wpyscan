import requests

class XML_RPC:
    def __init__(self, url):
        self.url = url

    def check_xml_rpc(self):
        try:
            xmlrpc_url = f"{self.url.rstrip('/')}/xmlrpc.php"
            response = requests.get(xmlrpc_url)

            if 200 <= response.status_code < 300:
                return True
        except requests.RequestException:
            pass

        return False

    def get_references(self):
        return [
            "http://codex.wordpress.org/XML-RPC_Pingback_API",
            "https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/",
            "https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/",
            "https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/",
            "https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/"
        ]