import pyotp

def generate_totp_secret():
    return pyotp.random_base32()

def generate_totp_uri(secret, username, issuer_name):
    return pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name=issuer_name)

def verify_totp_token(secret, token):
    return pyotp.TOTP(secret).verify(token)