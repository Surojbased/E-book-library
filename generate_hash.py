from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
hashed = bcrypt.generate_password_hash("test123").decode('utf-8')
print(hashed)
# $2b$12$X/vl2VNPQHR9EAm3XTqGY.sAiHxp.708PYTPv96jGXZdC51jGxNP6