from passlib.hash import pbkdf2_sha256
import test

hash = pbkdf2_sha256.encrypt("password", rounds=200000, salt_size=16)
print hash

#test.verify(hash)
