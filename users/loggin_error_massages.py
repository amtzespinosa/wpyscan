import random
from models.loggin_error_messages import UserLogin, TargetLogin

class LoginErrorMessages:
    def __init__(self, target):
        self.target = target

    def aggressive(self, opts={}):
        found = []
        for username in self.usernames(opts):
            password = self.generate_random_password()
            response = self.target.do_login(username, password)
            error = response.html.select_one('div#login_error').text.strip()

            if not error:  # Protection plugin / error disabled
                return found

            if "The password you entered for the username" in error or "Incorrect Password" in error:
                found.append(UserLogin(username, found_by='Login Error Messages', confidence=100))

        return found

    def usernames(self, opts={}):
        # Usernames from the potential Users found
        unames = [user.username for user in opts.get('found', [])]

        if 'list' in opts:
            unames += [uname.strip() for uname in opts['list']]

        return list(set(unames))

    def generate_random_password(self):
        return ''.join(random.choice('abcdef0123456789') for _ in range(8))


