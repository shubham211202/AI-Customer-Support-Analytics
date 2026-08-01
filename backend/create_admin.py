from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

user = User(
    name="Admin",
    email="admin@example.com",
    password=get_password_hash("admin123"),
    role="admin"
)

db.add(user)
db.commit()

print("Admin user created successfully")