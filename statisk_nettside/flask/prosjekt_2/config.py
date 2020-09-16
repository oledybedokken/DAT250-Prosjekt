from pathlib import Path
import os

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"

class ProductionConfig(Config):
    __secret = "admin" #"1lw3X$Jy*T5^hue"
    SECRET_KEY = os.environ.get("SECRET_KEY", __secret)
