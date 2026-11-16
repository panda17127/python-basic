# config.py —— 全项目的"设置中心"
# 取值优先级: 环境变量(临时手动指定) > .env 文件(本机偏好) > 下面的默认值(出厂设置)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 告诉 pydantic 去"运行目录"下找 .env 文件读配置(所以必须从项目根启动)
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "good-finds-server"   # 服务名:出现在 /docs 标题和 /api/test 返回里
    version: str = "1.3.1"                # 版本号:同上
    host: str = "127.0.0.1"               # 监听地址:127.0.0.1 = 只允许本机访问
    port: int = 8001                      # 监听端口:.env 里 PORT=8008 会覆盖这个默认值
    debug: bool = True                    # 调试模式:True 时 uvicorn 开热重载,改代码自动重启
    database_url: str = "sqlite:///./message.db"   # 数据库连接串:SQLite,库文件在项目根 message.db

settings = Settings()   # 单例:全项目只造一次,处处 import 这个实例