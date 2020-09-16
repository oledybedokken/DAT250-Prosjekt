from flask import (render_template, Blueprint, request, make_response, send_from_directory, jsonify)
import jwt
import decimal as decimal
from datetime import datetime
# from .api.utils import to_d128, withdraw, deposit
# from bson.decimal128 import create_decimal128_context, Decimal128
# from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
# from .config import Config
# from .model import clients
# from .model import get_account_num
# from .model import jti_backlist
# from luhn import verify
# from . import mongo 
# from . import bcrypt
# from . import f_jwt

# Copiert forklaring fra flask.palletsprojects.com:

# SECRET_KEY: 
# A secret key that will be used for securely signing the session cookie 
# and can be used for any other security related needs by extensions 
# or your application. It should be a long random string of bytes, 
# although unicode is accepted too.

