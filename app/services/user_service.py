from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserUpdatePartial

class UserService:
    
    @staticmethod
    def get_all_users(role: str = None, is_active: bool = None):
        filtered = users_db
        if role:
            filtered = [u for u in filtered if u["role"].lower() == role.lower()]
        if is_active is not None:
            filtered = [u for u in filtered if u["is_active"] == is_active]
        return filtered

    @staticmethod
    def get_user_by_id(user_id: int):
        for user in users_db:
            if user["id"] == user_id:
                return user
        return None

    @staticmethod
    def get_user_by_email(email: str):
        for user in users_db:
            if user["email"].lower() == email.lower():
                return user
        return None

    @staticmethod
    def create_user(user_data: UserCreate):
        new_id = max([u["id"] for u in users_db], default=0) + 1
        new_user = user_data.model_dump()
        new_user["id"] = new_id
        users_db.append(new_user)
        return new_user

    @staticmethod
    def update_user_complete(user_id: int, user_data: UserUpdate):
        for index, user in enumerate(users_db):
            if user["id"] == user_id:
                updated = user_data.model_dump()
                updated["id"] = user_id
                users_db[index] = updated
                return updated
        return None

    @staticmethod
    def update_user_partial(user_id: int, user_data: UserUpdatePartial):
        for index, user in enumerate(users_db):
            if user["id"] == user_id:
                update_data = user_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    users_db[index][key] = value
                return users_db[index]
        return None

    @staticmethod
    def delete_user(user_id: int):
        for index, user in enumerate(users_db):
            if user["id"] == user_id:
                users_db.pop(index)
                return True
        return False