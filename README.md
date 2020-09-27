# django_firebase_scrypt
A Django password hasher based off scrypt to use for user accounts imported from Firebase.

## Installation
Install dependencies according to your Python version and OS:
```
# Debian/Ubuntu
$ sudo apt-get install build-essential libssl-dev python-dev

# Fedora, RHEL
$ sudo yum install gcc openssl-devel python-devel

# Alpine Linux (Docker Containers)
$ apk add gcc openssl-dev python-dev

# (If you're on Python3, install the Python3 versions of the above packages)

# Mac
# Without setting the flags below, install will fail to find the necessary files
$ brew install openssl
$ export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
$ export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"
```

Then install this package from PyPI (https://pypi.org/project/django-firebase-scrypt/):
```
pip install django-firebase-scrypt
```

## Usage
Add this to your hashers `settings.py` like so
```
PASSWORD_HASHERS = (
  'django_firebase_scrypt.FirebaseScryptPasswordHasher',
  'django.contrib.auth.hashers.PBKDF2PasswordHasher',
  'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
  'django.contrib.auth.hashers.SHA1PasswordHasher',
  'django.contrib.auth.hashers.MD5PasswordHasher',
  'django.contrib.auth.hashers.CryptPasswordHasher',
  'django.contrib.auth.hashers.Argon2PasswordHasher',
  'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

# Retrieve these from  the Firebase console - see https://firebaseopensource.com/projects/firebase/scrypt/
FIREBASE_SIGNER_KEY = "jxspr8Ki0RYycVU8zykbdLGjFQ3McFUH0uiiTvC8pVMXAn210wjLNmdZJzxUECKbm0QsEmYUSDzZvpjeJ9WmXA=="
FIREBASE_SALT_SEPARATOR = "Bw=="
FIREBASE_ROUNDS = 8
FIREBASE_MEMCOST = 14
```


You can also move `FirebaseScryptPasswordHasher` to the bottom of your hashers if you only want to use it to validate 
old, migrated hashes instead of generating them for new users.

## Migration
Migrate your Firebase users to Django.  You can do so as follows:
```
# Grab your users and their password hashes using the Firebase auth:export command
$ npm install -g firebase-tools
$ firebase auth:export users.json
```

```
import json

import django
django.setup()
from django.contrib.auth import get_user_model

from django_firebase_scrypt import FirebaseScryptPasswordHasher

User = get_user_model()

with open("users.json", "r") as user_file:
    firebase_users = json.load(user_file)["users"]

for firebase_user in firebase_users:
    django_password = f"{FirebaseScryptPasswordHasher.algorithm}${firebase_user['salt']}${firebase_user['passwordHash']}"
    django_user = User(email=firebase_user["email"], password=django_password, ...any_other_user_fields)
    django_user.save()
```


