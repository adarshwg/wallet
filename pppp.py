import jwe

key = b'MySecretKey'
salt = b'pepper'

derived_key = jwe.kdf(key, salt)

encoded = jwe.encrypt(b'SuperSecretData', derived_key)

print(encoded)

jwe.decrypt(encoded, derived_key)  # b'SuperSecretData'