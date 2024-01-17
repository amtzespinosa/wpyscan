import requests
from avoidance.user_agents import get_random_user_agent

class UserPosts:
    def __init__(self, username, found_by, confidence):
        self.username = username
        self.found_by = found_by
        self.confidence = confidence

class TargetPosts:
    def __init__(self, homepage_url):
        self.homepage_url = homepage_url

    def get_response(self, url):
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        return response