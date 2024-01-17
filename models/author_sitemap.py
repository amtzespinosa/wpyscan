class UserSitemap:
    def __init__(self, username, found_by, confidence, interesting_entries):
        self.username = username
        self.found_by = found_by
        self.confidence = confidence
        self.interesting_entries = interesting_entries

class TargetSitemap:
    def __init__(self, base_url):
        self.base_url = base_url

    def url(self, path):
        return f"{self.base_url}/{path}"

