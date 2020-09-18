from flask import (render_template, Blueprint, request, make_response,
                   send_from_directory, jsonify)
from . import bcrypt
from . import jwt
import jwt
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, 
    get_jwt_identity, get_jwt_claims)                                                   # https://flask-jwt-extended.readthedocs.io/en/stable/tokens_from_complex_object/
from .model import unik_konto_nummer
import decimal as decimal
from .prosjekt_1.views import uttak
from datetime import datetime


# HUSK: 
# LAG AUTORISERINGS KODE OG IMPORT TIL HER!


# Copiert forklaring fra flask.palletsprojects.com: - Kan brukes?

# SECRET_KEY: 
# A secret key that will be used for securely signing the session cookie 
# and can be used for any other security related needs by extensions 
# or your application. It should be a long random string of bytes, 
# although unicode is accepted too.

