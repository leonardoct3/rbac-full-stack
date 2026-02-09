from entities.user import UserCreate
from models.user import User

class UserService:
    def create_user(self, user_create: UserCreate) -> User:
        # Here you would typically interact with the database to create a new user
        # For demonstration purposes, we'll just return a User instance based on the input
        new_user = User(id=user_create.id, name=user_create.name, fullname=user_create.fullname)
        return new_user