from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, _id, username, email, password):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def create_user(mongo, username, email, password):
        user_id = mongo.db.users.insert_one({"username": username, "email": email, "password": password}).inserted_id
        
        return User(user_id, username, email, password)

    @staticmethod
    def find_by_id(mongo, user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data["_id"]), user_data["username"], user_data["email"], user_data["password"])
        
        return None

    def reset_password(self, mongo, new_password_hash):
        mongo.db.users.update_one({"_id": ObjectId(self.id)}, {"$set": {"password": new_password_hash}})

    def delete_account(self, mongo):
        result = mongo.db.users.delete_one({"_id": ObjectId(self.id)})
        if result.deleted_count > 0:
            mongo.db.tasks.delete_one({"user_id": str(self.id)})
            return True
        
        return False

class UserTasks:
    def __init__(self, user_id, backlog=None, waiting=None, working=None, done=None):
        self.user_id = str(user_id)
        self.backlog = backlog if backlog is not None else []
        self.waiting = waiting if waiting is not None else []
        self.working = working if working is not None else []
        self.done = done if done is not None else []

    def save_to_db(self, mongo):
        mongo.db.tasks.update_one(
            {"user_id": self.user_id},
            {"$set": {
                "backlog": self.backlog,
                "waiting": self.waiting,
                "working": self.working,
                "done": self.done
            }},
            upsert=True
        )

    @staticmethod
    def load_from_db(mongo, user_id):
        task_data = mongo.db.tasks.find_one({"user_id": str(user_id)})
        if task_data:
            task_data.pop('_id', None)
            return UserTasks(**task_data)
        
        return UserTasks(user_id)
