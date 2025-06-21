from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class DBSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @property
    def postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    model_config = ConfigDict(env_file=".env", extra="allow")


class GenericSettings(BaseSettings):
    SUPER_ADMIN_LOGIN: str = "admin"
    SUPER_ADMIN_PASSWORD: str = "admin"

    model_config = ConfigDict(env_file=".env", extra="allow")


class JWTSettings(BaseSettings):
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_TIME: int = 600
    REFRESH_TOKEN_EXPIRE_TIME: int = 1209600

    model_config = ConfigDict(env_file=".env", extra="allow")


db_settings = DBSettings()
generic_settings = GenericSettings()
jwt_settings = JWTSettings()

