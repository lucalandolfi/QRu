# QRu
QRu (Q-are-you) is a QR code based authentication system. It's a web app, implemented using Flask microframework. It is intended to be used together with QRu-rasp https://github.com/lucalandolfi/QRu-rasp .
In order to authenticate users, it uses REST APIs of UniParthenope Esse3 instance.

## Install
QRu uses pip3 to manage dependencies, so it is required. To install it on debian-based systems
```
apt-get install python3-pip
```

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
First, create the database schema and create an admin user. Open a flask python shell from command line
```
flask shell
```
and, inside python shell, execute
```
from app.models import db, Admin
db.create_all()
a = Admin(username=someusername, password=somepassword)
db.session.add(a)
db.session.commit()
```

## Run
```
SECRET_KEY=yoursecretkey FLASK_APP=QRu.py FLASK_ENV=development flask run --host 0.0.0.0
```
or edit and run supplied test script
```
sh tests/test.sh
```

### Key generation
SECRET_KEY is a 32 byte, base64 encoded, URL safe string. It is used as key to encrypt and sign tokens and to generate API keys for QRu-rasp devices. A suitabable key can be generated with the following python code, using the same library used by QRu for encryption
 ```
from cryptography.fernet import Fernet
Fernet.generate_key().decode()
 ```
 the output is a string
 ```
 'GxdY_OX0vFPTc-fxClqZhI5zjNvhKPQls4uZeP_9Pwo='
```
## Usage
Once the server is up and running, using the web interface you need to generate one or more API keys, which need to be distributed to any raspberry pi running QRu-rasp application.
