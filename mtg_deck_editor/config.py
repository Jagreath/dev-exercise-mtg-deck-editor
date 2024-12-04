import os
BASE_DIR = os.path.abspath(os.getcwd())

class Config(object):
    ATOMIC_CONNECTION = ''
    DECKS_CONNECTION = ''

class DevConfig(Config):
    ATOMIC_CONNECTION = os.path.join(BASE_DIR, "sqlite/AllPrintings.sqlite")
    DECKS_CONNECTION = os.path.join(BASE_DIR, "sqlite/decks.sqlite")

_ENV_CONFIGS = {
    'dev': DevConfig,
}

APP_CONFIG = _ENV_CONFIGS['dev']
