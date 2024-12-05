import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_BINDS =  {
        "SETS": "",
        "DECKS": ""
    }

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "sqlite\\decks.sqlite")
    SQLALCHEMY_BINDS =  {
        "SETS": "sqlite:///" + os.path.join(basedir, "sqlite\\AllPrintings.sqlite"),
        "DECKS": "sqlite:///" + os.path.join(basedir, "sqlite\\decks.sqlite")
    }

_ENV_CONFIGS = {
    'dev': DevConfig,
}

APP_CONFIG = _ENV_CONFIGS['dev']
