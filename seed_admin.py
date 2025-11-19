from app import create_app
from extensions.db import db
from models.user import User
from models.admin_profile import AdminProfile

def seed_admin():
    app = create_app()
    with app.app_context():
        existing_admin = User.query.filter_by(role="admin").first()
        if existing_admin:
            print("Admin already exists. Skipping seeding.")
            return

        admin_email = "admin@system.com"
        admin_password = "Admin123!"   
        admin = User(email=admin_email, password=admin_password, role="admin")

        db.session.add(admin)
        db.session.flush()  
        staff_id = f"STF-{admin.user_id:06d}"

        # Create admin profile
        profile = AdminProfile(
            admin_id=admin.user_id,
            full_name="System Administrator",
            staff_id=staff_id,
            phone="08000000000"
        )

        db.session.add(profile)
        db.session.commit()

        print("✓ Super Admin seeded successfully!")
        print("Login with:")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        print(f"Staff ID: {staff_id}")

if __name__ == "__main__":
    seed_admin()
