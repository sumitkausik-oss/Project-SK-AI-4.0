import secrets
import hashlib

class KeyGenerator:
    def __init__(self):
        # Constants for identifying key types internally
        self._admin_salt = "SK_AI_SUPER_SECRET_ADMIN_SALT_v4"
        self._user_salt = "SK_AI_USER_SALT_365_v4"

    def _generate_key_hash(self, base_string: str, salt: str) -> str:
        """Generates a secure hash from a string and salt."""
        combined = base_string + salt
        return hashlib.sha256(combined.encode()).hexdigest()

    def generate_admin_lifetime_key(self, admin_identifier: str, platform: str = "WIN") -> str:
        """Generates a perpetual key linked to an admin ID or hardware ID with platform prefix."""
        random_part = secrets.token_hex(16)
        # Structured key base info
        key_base = f"LIFETIME-ADMIN-{admin_identifier}-{random_part}"
        key_hash = self._generate_key_hash(key_base, self._admin_salt)
        return f"{platform.upper()}-{key_hash}"

    def generate_user_yearly_key(self, platform: str = "WIN") -> str:
        """Generates a random key intended for 365 days with platform prefix."""
        random_part = secrets.token_hex(24)
        # Structured key base info
        key_base = f"YEARLY-USER-{random_part}"
        key_hash = self._generate_key_hash(key_base, self._user_salt)
        return f"{platform.upper()}-{key_hash}"

# Example Usage
if __name__ == "__main__":
    kg = KeyGenerator()
    print("Sample Admin Lifetime Key (e.g. for InventorSumeetKumar):")
    print(kg.generate_admin_lifetime_key("InventorSumeetKumar"))
    print("\nSample User Yearly Key (365 days):")
    print(kg.generate_user_yearly_key())
