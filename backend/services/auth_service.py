from backend.database.models import User
from backend.repositories.user_repository import UserRepository
from backend.security.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def register_user(self, name: str, email: str, password: str):
        existing_user = self.user_repository.find_by_email(email)

        if existing_user is not None:
            raise ValueError("E-mail já cadastrado.")

        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role="ANALYST"
        )

        return self.user_repository.save(user)

    def authenticate_user(self, email: str, password: str):
        user = self.user_repository.find_by_email(email)

        if user is None:
            raise ValueError("Credenciais inválidas.")

        if not verify_password(password, user.password_hash):
            raise ValueError("Credenciais inválidas.")

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }