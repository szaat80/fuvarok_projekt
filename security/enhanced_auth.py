import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
import bcrypt
from datetime import datetime, timedelta
from .security_config import SecurityConfig # Hozzáadva a typing import

class EnhancedAuthManager:
    """Fejlesztett autentikációs kezelő"""
    
    def __init__(self, db_handler):
        self.db = db_handler
        self.security_config = SecurityConfig()
        self.failed_attempts = {}
        self._setup_auth_table()
        self._setup_audit_log()
        self.create_admin_if_not_exists()

    def create_admin_if_not_exists(self):
        """Admin felhasználó létrehozása, ha még nem létezik"""
        try:
            result = self.db.execute_query("SELECT * FROM users WHERE username = ?", ('admin',))
            if not result:
                self.register_user('admin', 'admin123', 'admin')
        except Exception as e:
            logging.error(f"Admin létrehozási hiba: {str(e)}")
        
    def _setup_auth_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            login_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            password_changed_at TIMESTAMP,
            requires_password_change BOOLEAN DEFAULT FALSE
        )"""
        self.db.execute_query(query)
        
    def _setup_audit_log(self):
        """Audit log tábla létrehozása"""
        query = """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
        self.db.execute_query(query)

    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """Jelszó validáció"""
        if len(password) < self.security_config.MIN_PASSWORD_LENGTH:
            return False, f"A jelszónak minimum {self.security_config.MIN_PASSWORD_LENGTH} karakter hosszúnak kell lennie"
            
        if self.security_config.REQUIRE_SPECIAL_CHAR and not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
            return False, "A jelszónak tartalmaznia kell speciális karaktert"
            
        if self.security_config.REQUIRE_NUMBER and not any(c.isdigit() for c in password):
            return False, "A jelszónak tartalmaznia kell számot"
            
        if self.security_config.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, "A jelszónak tartalmaznia kell nagybetűt"
            
        return True, "Jelszó megfelelő"

    def register_user(self, username: str, password: str, role: str = 'user'):
        try:
            # Jelszó validáció
            is_valid, message = self._validate_password(password)
            if not is_valid:
                return False, message
            
            # Jelszó hashelés
            salt = bcrypt.gensalt()  # Itt generálunk új salt-ot
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
            data = {
                'username': username,
                'password_hash': password_hash.decode('utf-8'),
                'role': role,
                'password_changed_at': datetime.utcnow()
            }
        
            user_id = self.db.insert_record('users', data)
        
            # Audit log
            self._log_action(user_id, 'USER_REGISTERED', f'User {username} registered with role {role}')
        
            return True, "Regisztráció sikeres"
        
        except Exception as e:
            logging.error(f"Regisztrációs hiba: {str(e)}")
            return False, f"Regisztrációs hiba: {str(e)}"

    def authenticate(self, username: str, password: str, ip_address: Optional[str] = None) -> Tuple[bool, str]:
        """Fejlesztett hitelesítés"""
        try:
            # Ellenőrizzük a zárolást
            if self._is_account_locked(username):
                return False, "A fiók ideiglenesen zárolva van"
                
            result = self.db.execute_query(
                "SELECT id, password_hash, role, login_attempts FROM users WHERE username = ?", 
                (username,)
            )
            
            if not result:
                return False, "Hibás felhasználónév vagy jelszó"
                
            user = result[0]
            
            # Jelszó ellenőrzés
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # Sikeres bejelentkezés
                self._reset_login_attempts(user['id'])
                token = self._generate_token(user['id'], user['role'])
                self._update_last_login(user['id'])
                
                # Audit log
                self._log_action(user['id'], 'USER_LOGIN', f'Successful login from {ip_address}')
                
                return True, token
            else:
                # Sikertelen bejelentkezés
                self._increment_login_attempts(user['id'])
                
                # Audit log
                self._log_action(None, 'LOGIN_FAILED', 
                               f'Failed login attempt for user {username} from {ip_address}')
                
                return False, "Hibás felhasználónév vagy jelszó"
                
        except Exception as e:
            logging.error(f"Bejelentkezési hiba: {str(e)}")
            return False, f"Bejelentkezési hiba: {str(e)}"

    def _is_account_locked(self, username: str) -> bool:
        """Fiók zárolás ellenőrzése"""
        result = self.db.execute_query(
            "SELECT locked_until FROM users WHERE username = ?",
            (username,)
        )
        
        if result and result[0]['locked_until']:
            locked_until = datetime.fromisoformat(result[0]['locked_until'])
            if locked_until > datetime.utcnow():
                return True
                
        return False

    def _increment_login_attempts(self, user_id: int):
        """Sikertelen bejelentkezési kísérletek kezelése"""
        self.db.execute_query(
            """
            UPDATE users 
            SET login_attempts = login_attempts + 1,
                locked_until = CASE 
                    WHEN login_attempts + 1 >= ? 
                    THEN datetime('now', '+15 minutes')
                    ELSE NULL 
                END
            WHERE id = ?
            """,
            (self.security_config.MAX_LOGIN_ATTEMPTS, user_id)
        )

    def _reset_login_attempts(self, user_id: int):
        """Sikeres bejelentkezés után nullázás"""
        self.db.execute_query(
            "UPDATE users SET login_attempts = 0, locked_until = NULL WHERE id = ?",
            (user_id,)
        )

    def _generate_token(self, user_id: int, role: str) -> str:
        """Biztonságos token generálás"""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=self.security_config.TOKEN_EXPIRY_DAYS)
        }
        return jwt.encode(
            payload, 
            self.security_config.SECRET_KEY, 
            algorithm=self.security_config.TOKEN_ALGORITHM
        )

    def _log_action(self, user_id: Optional[int], action: str, details: str, ip_address: Optional[str] = None):
        """Audit log bejegyzés"""
        try:
            data = {
                'user_id': user_id,
                'action': action,
                'details': details,
                'ip_address': ip_address
            }
            self.db.insert_record('audit_log', data)
        except Exception as e:
            logging.error(f"Audit log hiba: {str(e)}")

    def _update_last_login(self, user_id: int):
            self.db.execute_query(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user_id,)
            )

    def verify_token(self, token: str) -> Tuple[bool, dict]:
        """Token ellenőrzés"""
        try:
            payload = jwt.decode(
                token, 
                self.security_config.SECRET_KEY, 
                algorithms=[self.security_config.TOKEN_ALGORITHM]
            )
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token lejárt"}
        except jwt.InvalidTokenError:
            return False, {"error": "Érvénytelen token"}

# Használati példa:
"""
# Inicializálás
auth_manager = EnhancedAuthManager(db_handler)

# Regisztráció
success, message = auth_manager.register_user("test_user", "SecurePass123!", "user")
if not success:
    print(f"Regisztrációs hiba: {message}")

# Bejelentkezés
success, token = auth_manager.authenticate("test_user", "SecurePass123!", "192.168.1.1")
if success:
    # Token használata további műveletekhez
    is_valid, payload = auth_manager.verify_token(token)
    if is_valid:
        user_id = payload['user_id']
        role = payload['role']
else:
    print(f"Bejelentkezési hiba: {token}")  # token itt hibaüzenet
"""