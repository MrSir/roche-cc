from __future__ import annotations

from functools import cached_property
from typing import Self, Type

from pydantic import BaseModel

from api.database.configuration import Base, DBSession
from api.database.models import User
from api.exceptions import ObjectNotFoundError
from api.validation.base_validators import Validator


class AuthenticatedController:
    @cached_property
    def user(self) -> User:
        # resolves the authenticated user from the request
        pass


class AuthorizedController(AuthenticatedController):
    def authorized_to(self, permission: str) -> Self:
        # Check if the user has the permission
        #   if they do NOT raise an UnauthorizedError
        #       the UnauthorizedError should be caught and return 403 Forbidden Response by the API
        return self


class ValidatedController:
    def validate(self, validator: Validator) -> Self:
        # Check if the incoming payload is valid
        #   if it is NOT raise a ValidationError
        #       the ValidationError should be caught and return a 422 Validation Error by the API with additional
        #       context
        validator.validate()

        return self


class ResourcefulController:
    model_class: Type[Base]

    def __init__(self):
        self.db_session = DBSession

    def get_object(self, identifier: int) -> Base:
        object_instance = self.db_session.query(self.model_class).filter(self.model_class.id == identifier).first()

        if object_instance is None:
            raise ObjectNotFoundError()

        return object_instance

