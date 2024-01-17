from bs4 import BeautifulSoup

class AuthorPosts:
    def __init__(self, target):
        self.target = target

    def passive(self):
        found_by_msg = 'Post Author - %s (Passive Detection)'
        usernames = self.usernames()

        return usernames

    def usernames(self):
        found = self.potential_usernames(self.target.homepage_url)

        return found if found else self.potential_usernames_from_posts()

    def potential_usernames(self, url):
        usernames = []

        response = self.target.get_response(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract usernames from links containing "author" in the href
        for link in soup.find_all('a', href=lambda href: href and 'author' in href):
            usernames.append([self.extract_username(link['href']), 'Author Pattern', 100])

        return usernames

    def extract_username(self, url):
        # Extract username from the URL, you might need to adjust this based on the actual URL structure
        return url.split('/')[-1]

    def potential_usernames_from_posts(self):
        usernames = []

        response = self.target.get_response(self.target.homepage_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract usernames from links in header.entry-header
        for post_url_node in soup.select('header.entry-header a'):
            url = post_url_node.get('href')

            if url:
                usernames += self.potential_usernames(url)

        return usernames
