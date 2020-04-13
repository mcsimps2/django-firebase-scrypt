import base64
import secrets
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.translation import ugettext_noop as _

import pyscryptfirebase


class FirebaseScryptPasswordHasher(BasePasswordHasher):
    algorithm = "fbscrypt"
    library = "fbscrypt"
    signer_key = base64.b64decode(settings.FIREBASE_SIGNER_KEY)
    salt_sep = base64.b64decode(settings.FIREBASE_SALT_SEPARATOR)
    rounds = settings.FIREBASE_ROUNDS
    memcost = settings.FIREBASE_MEMCOST

    def verify(self, password, encoded):
        algorithm, salt, hsh = encoded.split("$")
        hashp = pyscryptfirebase.encrypt(
            self.signer_key,
            base64.b64decode(salt),
            self.salt_sep,
            self.rounds,
            self.memcost,
            password
        )
        return secrets.compare_digest(base64.b64encode(hashp).decode("utf8"), hsh)

    def encode(self, password, salt):
        hsh = base64.b64encode(
            pyscryptfirebase.encrypt(
                self.signer_key,
                base64.b64decode(salt),
                self.salt_sep,
                self.rounds,
                self.memcost,
                password
            )
        )
        return "$".join([self.algorithm, salt, hsh.decode("utf8")])

    def safe_summary(self, encoded):
        algorithm, salt, hsh = encoded.split('$')
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('salt'), mask_hash(salt, show=2)),
            (_('hash'), mask_hash(hsh)),
        ])
