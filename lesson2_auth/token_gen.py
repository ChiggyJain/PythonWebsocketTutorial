import jwt

SECRET_KEY = "MY_SUPER_SECRET_KEY"
token = jwt.encode({"username": "chirag"}, SECRET_KEY, algorithm="HS256")
print("Your Token:", token)
