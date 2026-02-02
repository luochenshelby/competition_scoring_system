import hashlib

password = "admin789"
hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"SHA-256哈希值: {hashed}")