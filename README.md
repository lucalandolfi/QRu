# QRu
QRu (Q-are-you) is a QR code based authentication system. It's a web app, implemented using Flask microframework. It is intended to be used together with QRu-rasp https://github.com/lucalandolfi/QRu-rasp .

## Prerequisites
QRu uses pip3 to manage dependencies, so it is required. To install it on debian-based systems
```
apt-get install python3-pip
```
## Install

### Download
```
git clone https://github.com/lucalandolfi/QRu.git
```
### Setup
Create virtual environment and install dependencies
```
cd QRu
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

### Database creation
First, create the database schema and create an admin user
```
flask shell
from app.models import db, Admin
db.create_all()
a = Admin(username=someusername, password=somepassword)
db.session.add(a)
db.session.commit()
exit()
```

## Run
```
SECRET_KEY=yoursecretkey FLASK_APP=QRu.py FLASK_ENV=development flask run --host 0.0.0.0
```
or edit and run supplied test script
```
sh tests/test.sh
```
SECRET_KEY is a 32 byte, base64 encoded, URL safe string which is used as key to encrypt and sign token and to generate API keys for QRu-rasp devices. 
