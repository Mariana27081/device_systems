from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserUpdatePartial

class UserService:
    
    @staticmethod
    def get_all_users(role: str = None, is_active: bool = None):
        """Retorna todos los usuarios, permitiendo filtros opcionales."""
        filtered_users = users_db
        if role:
            filtered_users = [u for u in filtered_users if u["role"].lower() == role.lower()]
        if is_active is not None:
            filtered_users = [u for u in filtered_users if u["is_active"] == is_active]
        return filtered_users

    @staticmethod
    def get_user_by_id(user_id: int):
        """Busca un usuario por su ID."""
        for user in users_db:
            if user["id"] == user_id:
                return user
        return None

    @staticmethod
    def get_user_by_email(email: str):
        """Busca un usuario por su correo electrónico."""
        for user in users_db:
            if user["email"].lower() == email.lower():
                return user
        return None

    @staticmethod
    def create_user(user_data: UserCreate):
        """Crea un nuevo usuario asignándole un ID autoincremental."""
        new_id = max([u["id"] for u in users_db], default=0) + 1
        new_user = user_data.model_dump()
        new_user["id"] = new_id
        users_db.append(new_user)
        return new_user

    @staticmethod
    def update_user_complete(user_id: int, user_data: UserUpdate):
        """Reemplaza completamente un usuario existente."""
        for index, user in enumerate(users_db):
            if user["id"] == user_id:
                updated_user = user_data.model_dump()
                updated_user["id"] = user_id
                users_db[index] = updated_user
                return updated_user
        return None

    @staticmethod
    def update_user_partial(user_id: int, user_data: UserUpdatePartial):
        """Modifica parcialmente un usuario existente."""
        for index, user in enumerate(users_db):
            if user["id"] == user_id:
                # Extraemos solo los campos que envió el cliente (excluyendo los no enviados)
                update_data = user_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    users_db[index][key] = value
                return users_db[index]
        return None

    @staticmethod
    def delete_user(user_id: int):
        """Elimina un usuario de la lista."""
        for index, user in enumerate(users_db):
            if user["id"] == user_id:
                users_db.pop(index)
                return True
        return False