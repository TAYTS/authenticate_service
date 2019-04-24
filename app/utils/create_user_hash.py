import hashlib


def create_user_hash(username):
    unhashed_user = "email: " + username + "ESC-Accenture"
    hashed_user = hashlib.sha256(unhashed_user.encode("UTF-8")).hexdigest()

    return hashed_user
