from app import create_app
from extensions.db import db
from models.user import User

def seed_admin():
    app = create_app()
    with app.app_context():
        existing_admin = User.query.filter_by(role="admin").first()
        if existing_admin:
            print("Admin already exists:", existing_admin.email)
            return

        admin = User(
            email="superadmin@gmail.com",
            password="Admin123!",
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Super Admin created successfully!")
        print("Email: superadmin@gmail.com")
        print("Password: Admin123!")

if __name__ == "__main__":
    seed_admin()
