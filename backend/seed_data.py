from app.core.database import SessionLocal, engine, Base
from app.models.auth import Workspace, User
from app.core.security import get_password_hash

def seed():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Create Default Workspace
        ws_id = '11111111-1111-1111-1111-111111111111'
        ws = db.query(Workspace).filter(Workspace.name=='Default').first()
        if not ws:
            ws = Workspace(id=ws_id, name='Default')
            db.add(ws)
            db.commit()
            print("Workspace 'Default' created.")
        else:
            ws_id = str(ws.id)
            print("Workspace 'Default' already exists.")

        # 2. Create Admin User - hash password at runtime
        admin_password = "admin123"
        admin_hash = get_password_hash(admin_password)
        print(f"Generated password hash for 'admin123'")
        
        existing_user = db.query(User).filter(User.email=='admin@nexerp.com').first()
        if not existing_user:
            admin = User(
                id='22222222-2222-2222-2222-222222222222', 
                workspace_id=ws_id, 
                email='admin@nexerp.com', 
                full_name='Administrator', 
                hashed_password=admin_hash, 
                is_active=True, 
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("User 'admin@nexerp.com' created.")
        else:
            # Update password
            existing_user.hashed_password = admin_hash
            db.commit()
            print("User 'admin@nexerp.com' updated with correct password.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
