import requests

class Headers:
    def __init__(self, url):
        self.url = url

    def analyze_headers(self):
        try:
            response = requests.get(self.url)
            if 200 <= response.status_code < 300:
                print("[+] Headers:")
                print("    [+] Interesting Entries:")

                interesting_entries = [
                    "server",
                    "x-powered-by",
                    "x-cache-enabled",
                    "x-httpd",
                    "host-header",
                    "x-proxy-cache",
                    "strict-transport-security",
                    "content-security-policy",
                    "x-frame-options",
                    "x-xss-protection",
                    "x-content-type-options",
                    "referrer-policy",
                    "feature-policy",
                ]

                for entry in interesting_entries:
                    header_value = response.headers.get(entry)
                    if header_value:
                        print(f"     |- {entry}: {header_value}")
                return "     |- Found By: Headers (Passive Detection)"
            else:
                return f"[-] Failed to retrieve headers. Status Code: {response.status_code}"

        except requests.RequestException as e:
            return f"[-] An error occurred: {e}"
