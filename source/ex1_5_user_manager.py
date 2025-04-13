class DuplicateUser(Exception):
    pass


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username: str, email: str) -> True:
        if username in self.users:
            raise DuplicateUser("User already exist")
        self.users[username] = email
        return True

    def get_user_email(self, username: str) -> str:
        return self.users.get(username, "Upss...")
