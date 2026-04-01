from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Echo Investment Assistant"
    database_url: str = "sqlite:///./echo.db"
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "root"
    mysql_database: str = "echo"
    quote_sync_enabled: bool = True
    quote_sync_interval_seconds: int = 1800

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def mysql_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )


settings = Settings()
