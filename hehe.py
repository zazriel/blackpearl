

import hashlib


username = input("Enter username: ")
print(hashlib.md5(username.encode()).hexdigest()[:6])