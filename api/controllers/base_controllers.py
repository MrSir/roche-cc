from __future__ import annotations

from typing import Self, Type

from sqlalchemy.orm import Session

from api.database.configuration import Base
from api.database.models import User
from api.exceptions import ObjectNotFoundError
from api.validation.base_validators import Validator


class DBSessionController:
    def __init__(self, db_session: Session):
        self.db_session = db_session


class AuthenticatedController(DBSessionController):
    _user: User | None = None

    @property
    def user(self) -> User:
        if self._user is None:
            # TODO: resolves the authenticated user from the request
            self._user = self.db_session.query(User).filter(User.id == 1).first()

        return self._user


class AuthorizedController(AuthenticatedController):
    def authorized_to(self, permission: str) -> Self:
        # Check if the user has the permission
        #   if they do NOT, raise an UnauthorizedError
        #       the UnauthorizedError should be caught and return 403 Forbidden Response by the API
        return self


class ValidatedController:
    def validate(self, validator: Validator) -> Self:
        # Check if the incoming payload is valid
        #   if it is NOT, raise a RequestValidationError
        #       the RequestValidationError should be caught and return a 422 Validation Error by the API with additional
        #       context
        validator.validate()

        return self


class ResourcefulController(DBSessionController):
    model_class: Type[Base]

    def get_object(self, identifier: int) -> Base:
        object_instance = self.db_session.query(self.model_class).filter(self.model_class.id == identifier).first()

        if object_instance is None:
            raise ObjectNotFoundError()

        return object_instance
