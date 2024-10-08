"""This module contains utility functions that support various parts of the application."""

import hashlib

def password_hash(password):
    """Hashes password using SHA-256 algorithm."""
    return hashlib.sha256(bytes(password, "utf-8")).hexdigest()
