class DuplicateUser(Exception):
    pass


class Database:
    def __init__(self):
        self.users = {}

    def add_user(self, username: str, email: str) -> True:
        if username in self.users:
            raise DuplicateUser("User already exist")
        self.users[username] = email
        return True

    def get_user_email(self, username: str) -> [str, None]:
        return self.users.get(username, None)

    def delete_user(self, username: str) -> True:
        if username in self.users:
            self.users.pop(username)
            return True

    def clean(self):
        self.users = {}
        # pass