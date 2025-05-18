import hashlib

def hash_password(password):
    """
    Hashes a password using the SHA-256 algorithm.

    Args:
        password (str): The password string to hash.

    Returns:
        str: The hexadecimal representation of the hashed password.
    """
    # Encode the password string to bytes before hashing
    return hashlib.sha256(password.encode()).hexdigest()

# This file contains utility functions that can be used across the application.
# Currently, it only includes the password hashing function.
# More general utility functions can be added here in the future.
