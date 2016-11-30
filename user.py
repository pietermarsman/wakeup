from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def to_json(self):
        return {'id': self.id, 'logged_in': self.is_authenticated}

    @staticmethod
    def get(user_id):
        if user_id == "1":
            return User(user_id)
        return None