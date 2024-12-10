import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = ""

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "sqlite\\decks.sqlite")

_ENV_CONFIGS = {
    'dev': DevConfig,
}

APP_CONFIG = _ENV_CONFIGS['dev']
