from flask import request, make_response
from itsdangerous import URLSafeTimedSerializer
from cryptography.fernet import Fernet

from . import app
from .models import User, Device

@app.route('/verify', methods = ['POST'])
def verify():
    params = request.get_json()
    key = params.get('key')
    token = params.get('token')

    if key is None:
        return make_response('API key is required', 401)

    if token is None:
        return make_response('Missing token', 400)

    ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    fb = Fernet(app.config['SECRET_KEY'].encode())

    try:
        device = Device.query.filter_by(key=key).first()
        device_name = device.name
    except:
        return make_response('Invalid API key', 401)

    try:
        decrypted_token = fb.decrypt(token.encode()).decode()
        username = ts.loads(decrypted_token,
            max_age = app.config['MAX_TOKEN_AGE'])['username']
    except:
        return make_response('Invalid token', 403)

    device = Device.query.filter_by(name=device_name).first()
    user = User.query.filter_by(username=username).first()

    if device.mode == 'whitelist' and user not in device.whitelist:
        return make_response('User not allowed', 403)

    return make_response('Ok', 200)
