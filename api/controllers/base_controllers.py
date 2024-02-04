from __future__ import annotations

from functools import cached_property
from typing import Self, Type

from sqlalchemy.orm import Session

from api.database.configuration import Base, DBSession
from api.database.models import User
from api.exceptions import ObjectNotFoundError
from api.validation.base_validators import Validator


class AuthenticatedController:
    _user: User | None = None

    @property
    def user(self) -> User:
        if self._user is None:
            # TODO: resolves the authenticated user from the request
            self._user = self.db_session.query(User).filter(User.id == 1).first()
            # self._user =

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


class ResourcefulController:
    model_class: Type[Base]

    def __init__(self):
        self._db_session: Session = DBSession()

    @property
    def db_session(self) -> Session:
        return self._db_session

    def get_object(self, identifier: int) -> Base:
        object_instance = self.db_session.query(self.model_class).filter(self.model_class.id == identifier).first()

        if object_instance is None:
            raise ObjectNotFoundError()

        return object_instance

