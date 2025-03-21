import base64
import hashlib
import os

# Генерируем случайный `code_verifier`
code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode()

# Создаем SHA-256 хеш от `code_verifier`
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()

print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")