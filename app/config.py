from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """项目配置"""

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./lianxi.db" 

    app_name: str = "good-finds-server"
    version: str = "1.3.0"
    host: str = "127.0.0.1"
    port: int = 8001
    debug: bool = True

settings = Settings()