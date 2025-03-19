from flask_migrate import upgrade
from app import create_app
from app.init_admin import create_admin_if_not_exists

app = create_app()

with app.app_context():
    upgrade()
    create_admin_if_not_exists()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
