import secrets

class SecurityConfig:
    def __init__(self):
        self.SECRET_KEY = secrets.token_urlsafe(32)
        self.MIN_PASSWORD_LENGTH = 8
        self.TOKEN_EXPIRY_DAYS = 1
        self.REQUIRE_SPECIAL_CHAR = False  
        self.REQUIRE_NUMBER = False        
        self.REQUIRE_UPPERCASE = False     
        self.MAX_LOGIN_ATTEMPTS = 3
        self.TOKEN_ALGORITHM = 'HS256'