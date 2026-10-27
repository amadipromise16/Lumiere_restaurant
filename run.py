import os
import sys
from pathlib import Path

# Add current workspace root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'py'))

from app import app, db, seed_data

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    print("=" * 60)
    print(" Lumière Restaurant Application Started Successfully!")
    print(" Access URL: http://127.0.0.1:5000")
    print(" Admin Login: admin@lumiere.com | Password: Admin@Lumiere2025")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
