import uuid
from flask import session
from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)
        return None

    @staticmethod
    def login_valid(email, password):
        # User.login_valid("ddvidenov@gmail.com", "1234")
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        # check whether a users email matches password they sent us
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User doesn't exist, so we can create it
            return False

    @staticmethod
    def login(user_email):
        # Login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())