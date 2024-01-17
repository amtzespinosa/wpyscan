import requests

class UserLogin:
    def __init__(self, username, found_by, confidence):
        self.username = username
        self.found_by = found_by
        self.confidence = confidence

class TargetLogin:
    def __init__(self, base_url):
        self.base_url = base_url

    def do_login(self, username, password):
        login_url = self.url('wp-login.php')
        data = {'log': username, 'pwd': password, 'wp-submit': 'Log In'}
        return requests.post(login_url, data=data)

    def url(self, path):
        return f"{self.base_url}/{path}"

