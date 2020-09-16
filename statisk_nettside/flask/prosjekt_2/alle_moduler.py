from flask import (render_template, Blueprint, request, make_response, send_from_directory, jsonify)
import jwt
import decimal as decimal
from datetime import datetime


# Copiert forklaring fra flask.palletsprojects.com:

# SECRET_KEY: 
# A secret key that will be used for securely signing the session cookie 
# and can be used for any other security related needs by extensions 
# or your application. It should be a long random string of bytes, 
# although unicode is accepted too.

