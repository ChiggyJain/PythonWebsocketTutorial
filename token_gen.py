import jwt

SECRET_KEY = "MY_SUPER_SECRET_KEY"

token = jwt.encode({"username": "chirag"}, SECRET_KEY, algorithm="HS256")
print("Your Token:", token)

#print(jwt.encode({"username": "chirag", "role": "student"}, SECRET_KEY, algorithm="HS256"))
#print(jwt.encode({"username": "teacher1", "role": "teacher"}, SECRET_KEY, algorithm="HS256"))