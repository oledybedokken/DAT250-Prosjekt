from pathlib import Path
import os

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"

class ProdConfig(Config):
    __nokkel = "admin" #"1lw3X$Jy*T5^hue"
    SECRET_KEY = os.environ.get("SECRET_KEY", __nokkel)
