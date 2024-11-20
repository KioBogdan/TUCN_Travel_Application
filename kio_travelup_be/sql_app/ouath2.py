from fastapi import Form

class OAuth2PasswordRequestFormEmail:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password