from flask import Flask
from flask_bcrypt import Bcrypt                                 # Sikkerhet mot gpu-angrep
from flask_jwt_extended import JWTManager                       # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/

# Bcrypt: (bcrypt-hashing)

# Bruker en hash for å være de-optimalisert fra gpu-angrep. 
# Med vilje strukturert for å være treg for sensitiv data (passord...)

bcrypt = Bcrypt()
jwt = JWTManager()

