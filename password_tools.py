from flask_bcrypt import generate_password_hash, check_password_hash

def hashpw(password):
    return generate_password_hash(password).decode('utf-8')

def checkpw(pwhash, password):
    return check_password_hash(pwhash, password)
