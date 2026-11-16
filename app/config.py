from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env") 

    app_name: str = "good-finds-server"
    version: str = "1.3.1"
    host: str = "127.0.0.1"
    port: int = 8001
    debug: bool = True

settings = Settings()   # 单例:全项目只造一次,处处 import 这个实例