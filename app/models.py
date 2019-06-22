from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

is_authorized = db.Table('association', db.Model.metadata,
    db.Column('device.id', db.Integer, db.ForeignKey('device.id')),
    db.Column('user.id', db.String(64), db.ForeignKey('user.id')))

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    key = db.Column(db.String(64), unique=True, nullable=False)
    mode = db.Column(db.Enum('all', 'whitelist'), nullable=False)
    whitelist = db.relationship(
        'User',
        secondary=is_authorized,
        back_populates='devices')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    devices = db.relationship(
        'Device',
        secondary=is_authorized,
        back_populates='whitelist')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
