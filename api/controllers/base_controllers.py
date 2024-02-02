from api.database.models import User


class AuthenticatedController:
    def user(self) -> User:
        # resolves the authenticated user from the request
        pass