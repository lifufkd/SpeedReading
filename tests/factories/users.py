import factory
import copy

from constants.users import UsersConstants
from src.models.users import Users
from src.core.jwt import get_password_hash
from src.schemas.enums import UsersRoles


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Users

    login = factory.Faker("user_name")
    password_hash = get_password_hash(UsersConstants.DEFAULT_PASSWORD)
    email = factory.Faker("email")
    role = UsersRoles.USER

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        obj = model_class(*args, **kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
