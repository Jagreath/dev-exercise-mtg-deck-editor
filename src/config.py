import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "NOTAVERYBIGSECRETATALL"
    SQLALCHEMY_DATABASE_URI = ""

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "../sqlite\\deck_editor_db.sqlite")

class TestConfig(Config):
    SECRET_KEY = os.environ.get("FLASK_SECRET","")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","").replace("postgres://", "postgresql://")

_ENV_CONFIGS = {
    "dev": DevConfig,
    "test": TestConfig
}

APP_CONFIG = _ENV_CONFIGS["dev"]
