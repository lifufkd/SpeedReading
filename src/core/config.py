from pydantic_settings import BaseSettings
from pydantic import ConfigDict

from src.schemas.enums import LoggerLevels


class DBSettings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_DATABASE: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    TEST_DB_USER: str = "postgres"
    TEST_DB_PASSWORD: str = "postgres"
    TEST_DB_DATABASE: str = "test_postgres"
    TEST_DB_HOST: str = "localhost"
    TEST_DB_PORT: int = 5432

    @property
    def async_postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    @property
    def test_async_postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_DATABASE}"

    @property
    def sync_postgresql_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    model_config = ConfigDict(env_file=".env", extra="allow")


class GenericSettings(BaseSettings):
    SUPER_ADMIN_LOGIN: str = "admin"
    SUPER_ADMIN_PASSWORD: str = "Admin123@"

    model_config = ConfigDict(env_file=".env", extra="allow")


class JWTSettings(BaseSettings):
    # Generic jwt settings
    authjwt_secret_key: str
    authjwt_denylist_enabled: bool = True
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_access_token_expires: int = 60 * 15  # 15 minutes
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 7  # 7 days

    # Access cookie settings
    authjwt_access_cookie_path: str = "/"
    authjwt_access_cookie_samesite: str = "none"
    authjwt_access_cookie_secure: bool = False
    authjwt_access_cookie_max_age: int = 60 * 15  # 15 minutes

    # Refresh cookie settings
    authjwt_refresh_cookie_path: str = "/"
    authjwt_refresh_cookie_samesite: str = "none"
    authjwt_refresh_cookie_secure: bool = False
    authjwt_refresh_cookie_max_age: int = 60 * 60 * 24 * 7  # 7 days

    model_config = ConfigDict(env_file=".env", extra="allow")


class RedisSettings(BaseSettings):
    REDIS_USER: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_DATABASE: int = 0
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def redis_url(self):
        if self.REDIS_USER:
            redis_user = self.REDIS_USER
        else:
            redis_user = ""
        if self.REDIS_PASSWORD:
            redis_password = self.REDIS_PASSWORD
        else:
            redis_password = ""
        return f"redis://{redis_user}:{redis_password}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"

    model_config = ConfigDict(env_file=".env", extra="allow")


class CORSSettings(BaseSettings):
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    CORS_ALLOWED_ORIGINS: list[str] = []


class LoggerSettings(BaseSettings):
    LOG_LEVEL: LoggerLevels = LoggerLevels.INFO
    LOG_FILE_PATH: str = "app_data/logs/app.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "7 days"
    LOG_COMPRESSION: str = "gz"


db_settings = DBSettings()
generic_settings = GenericSettings()
jwt_settings = JWTSettings()
redis_settings = RedisSettings()
cors_settings = CORSSettings()
logger_settings = LoggerSettings()

