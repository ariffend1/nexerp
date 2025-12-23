from app.core.database import SessionLocal
from app.models.auth import User

db = SessionLocal()
user = db.query(User).filter(User.email == "admin@nexerp.com").first()
if user:
    # This is the hash for "admin123"
    # $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTEMbOAAGgP9nK
    user.hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTEMbOAAGgP9nK"
    db.commit()
    print("Password updated successfully!")
else:
    print("User not found!")
db.close()
