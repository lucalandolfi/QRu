from flask import Flask, request, make_response, render_template
from flask import url_for, session, redirect, abort, flash
import base64
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer
from io import BytesIO
import qrcode
from cryptography.fernet import Fernet

from . import app
from .forms import LoginForm, NewDeviceForm, SetDeviceForm
from .forms import DeleteDeviceForm, AuthorizeForm
from .models import db, Admin, User, Device
from .utils import login_required, cineca

@app.route('/')
def index():
    if session.get('admin') is True:
        return redirect(url_for('admin'))
    elif session.get('data') is not None:
        return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        q = Admin.query.filter_by(
            username=form.username.data,
            password=form.password.data).all()

        if len(q) != 0:
            session['username'] = form.username.data
            session['password'] = form.password.data
            session['admin'] = True
            session['data'] = {}
            return redirect(url_for('admin'))
        else:
            resp = cineca(form.username.data, form.password.data)
            if resp.status_code == 200:
                session['username'] = form.username.data
                session['password'] = form.password.data
                session['admin'] = False
                session['data'] = resp.json()
                return redirect(url_for('user'))
        flash("Username/password specified is not valid")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['username'] = None
    session['password'] = None
    session['admin'] = None
    session['data'] = None
    return redirect(url_for('index'))


@app.route('/user')
@login_required('user')
def user():
    firstName = session['data']['user']['firstName']
    lastName = session['data']['user']['lastName']
    return render_template('user.html', firstName=firstName, lastName=lastName)


@app.route('/admin')
@login_required('admin')
def admin():
    return render_template('admin.html',
        username = session.get('username'),
        device_list = Device.query.all())


# Generates a signed, timestamped token using the username of the user,
# and then convert it to a QR code
@app.route('/generate')
@login_required('user')
def generate():
    # generate temporized token and encrypt it
    ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    fb = Fernet(app.config['SECRET_KEY'].encode())

    token = ts.dumps({'username':session['username']})
    secure_token = fb.encrypt(token.encode()).decode()
    # convert to QR, PNG format, in memory
    image = BytesIO()
    qrcode.make(secure_token).save(image, format='png')
    # convert PNG to base64 for display in <img> tag
    image = base64.b64encode(image.getvalue()).decode("ascii")
    return make_response(image, 200)


@app.route('/deletedevice', methods = ['GET', 'POST'])
@login_required('admin')
def deletedevice():
    form = DeleteDeviceForm()
    if form.validate_on_submit():
        device = form.device.data
        # generate api ForeignKey
        try:
            d = Device.query.filter_by(name=device).first()
            db.session.delete(d)
            db.session.commit()
            flash('Device deleted')
        except:
            flash('Error')
        return redirect(url_for('.admin'))
    return render_template('crud.html', form=form,
        banner='Delete device')


@app.route('/newdevice', methods = ['GET', 'POST'])
@login_required('admin')
def newdevice():
    form = NewDeviceForm()
    if form.validate_on_submit():
        device = form.device.data
        mode = form.mode.data
        # sign with timestamp the device name to obtain
        # the API key
        ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        key = ts.dumps({'name': device}).split('.')[-1]
        try:
            d = Device(name=device, key=key, mode=mode)
            db.session.add(d)
            db.session.commit()
            flash('Device added')
        except:
            flash('Error')
        return redirect(url_for('admin'))
    return render_template('crud.html', form=form,
        banner='Add new authenticator device')


@app.route('/authorize', methods = ['GET', 'POST'])
@login_required('admin')
def authorize():
    form = AuthorizeForm()
    if form.validate_on_submit():
        username = form.username.data
        device = form.device.data
        try:
            u = User.query.filter_by(username=username).first()
            if u is None:
                u = User(username=username)
            d = Device.query.filter_by(name=device).first()
            d.whitelist.append(u)
            db.session.commit()
            flash('Authorized')
        except:
            flash('Error')
        return redirect(url_for('admin'))
    return render_template('crud.html', form=form,
        banner='Authorize user to access device')


@app.route('/revoke', methods = ['GET', 'POST'])
@login_required('admin')
def revoke():
    form = AuthorizeForm()
    if form.validate_on_submit():
        username = form.username.data
        device = form.device.data
        try:
            u = User.query.filter_by(username=username).first()
            d = Device.query.filter_by(name=device).first()
            d.whitelist.remove(u)
            db.session.commit()
            flash('Revoked')
        except:
            flash('Error')
        return redirect(url_for('admin'))
    return render_template('crud.html', form=form,
        banner='Revoke authorization to access device')


@app.route('/setdevice', methods = ['GET', 'POST'])
@login_required('admin')
def setdevice():
    form = SetDeviceForm()
    if form.validate_on_submit():
        device = form.device.data
        mode = form.mode.data
        try:
            d = Device.query.filter_by(name=device).first()
            d.mode = mode
            db.session.commit()
            flash('Modified')
        except:
            flash('Error')
        return redirect(url_for('admin'))
    return render_template('crud.html', form=form,
        banner='Edit access mode for a device')
