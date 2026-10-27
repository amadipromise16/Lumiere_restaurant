import os
from pathlib import Path
from datetime import datetime
import jinja2
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
    send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# Base directory for the repository root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
dotenv_path = BASE_DIR / '.env'
if not dotenv_path.exists():
    dotenv_path = BASE_DIR / 'env' / '.env'
load_dotenv(dotenv_path)

# Initialize Flask Application with explicit template and static paths
templates_dir = BASE_DIR / 'templates'
static_dir = BASE_DIR / 'static'

app = Flask(
    __name__,
    template_folder=str(templates_dir),
    static_folder=str(static_dir)
)

# Robust Multi-Directory Jinja Loader (checks templates/ and Assects/)
search_template_dirs = [
    str(BASE_DIR / 'templates'),
    str(BASE_DIR / 'Assects'),
    str(Path(__file__).resolve().parent / 'templates'),
]
app.jinja_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(p) for p in search_template_dirs if os.path.exists(p)
])

# Application Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'lumiere-luxury-secret-key-2025-secure')
db_file = BASE_DIR / 'lumiere.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', f'sqlite:///{db_file.as_posix()}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'
login_manager.login_message = 'Please sign in to access your table reservations.'
login_manager.login_message_category = 'info'


# --- Static Fallback Routes ---
@app.route('/css/<path:filename>')
def serve_css(filename):
    target = static_dir / 'css'
    if not (target / filename).exists():
        target = BASE_DIR / 'css'
    return send_from_directory(str(target), filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    target = static_dir / 'js'
    if not (target / filename).exists():
        target = BASE_DIR / 'js'
    return send_from_directory(str(target), filename)


# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    table_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='CONFIRMED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GalleryPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('gallery_photo.id'), nullable=False)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Database Initialization & Seeding ---
def seed_data():
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@lumiere.com')
    admin_pass = os.getenv('ADMIN_PASSWORD', 'Admin@Lumiere2025')

    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            name='Executive Administrator',
            email=admin_email,
            password_hash=generate_password_hash(admin_pass),
            is_admin=True
        )
        db.session.add(admin)

    if MenuItem.query.count() == 0:
        initial_menu = [
            MenuItem(
                name="Truffle Tagliatelle",
                description="House-made egg pasta, wild forest chanterelles, 24-month aged parmesan cream, black truffle oil",
                price=28.00,
                category="pasta",
                image_url="https://images.unsplash.com/photo-1556761223-4c4282c73f77?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Herb-Crusted Filet Mignon",
                description="Prime grass-fed beef tenderloin, roasted black garlic, glazed heirloom carrots, vintage Cabernet jus",
                price=46.00,
                category="mains",
                image_url="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Burrata & Poached Pear Salad",
                description="Artisanal Puglia burrata, organic baby arugula, candied walnuts, pomegranate molasses, citrus vinaigrette",
                price=18.00,
                category="salads",
                image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Valrhona Chocolate Fondant",
                description="Warm molten 70% dark chocolate center, lavender blossom gelato, raspberry coulis, gold leaf",
                price=14.00,
                category="desserts",
                image_url="https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Lobster & Saffron Ravioli",
                description="Hand-rolled Maine lobster parcels, brown butter sage emulsion, crispy parmesan tuile",
                price=32.00,
                category="pasta",
                image_url="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Wild Morel Mushroom Risotto",
                description="Acquerello carnaroli rice, white truffle oil, shaved aged pecorino, micro watercress",
                price=28.00,
                category="mains",
                image_url="https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Heritage Roasted Beet Salad",
                description="Golden & ruby beets, whipped goat cheese medallion, spiced pecans, 12-year Modena balsamic",
                price=16.00,
                category="salads",
                image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80"
            ),
            MenuItem(
                name="Artisan Reserve Sparkling Cuvée",
                description="Prestige brut reserve, crisp notes of green apple, elderflower blossoms, and delicate effervescence",
                price=14.00,
                category="beverages",
                image_url="https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=800&q=80"
            )
        ]
        for item in initial_menu:
            db.session.add(item)

    if GalleryPhoto.query.count() == 0:
        photos = [
            GalleryPhoto(image_url="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=800&q=80", title="Pan-Seared Diver Scallops"),
            GalleryPhoto(image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80", title="Grand Dining Salon"),
            GalleryPhoto(image_url="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80", title="Herb-Crusted Filet Mignon"),
            GalleryPhoto(image_url="https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=800&q=80", title="Intimate Velvet Booths"),
            GalleryPhoto(image_url="https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=800&q=80", title="Valrhona Chocolate Fondant"),
            GalleryPhoto(image_url="https://images.unsplash.com/photo-1556761223-4c4282c73f77?auto=format&fit=crop&w=800&q=80", title="Black Truffle Tagliatelle")
        ]
        for p in photos:
            db.session.add(p)

    db.session.commit()


# Ensure tables and seed data exist
with app.app_context():
    db.create_all()
    seed_data()


# --- Application Routes ---
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/menu')
def menu():
    category = request.args.get('category', 'all')
    if category == 'all':
        items = MenuItem.query.all()
    else:
        items = MenuItem.query.filter_by(category=category).all()

    carousel_photos = [
        "https://images.unsplash.com/photo-1556761223-4c4282c73f77?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=1200&q=80"
    ]
    return render_template('menu.html', items=items, active_category=category, carousel_photos=carousel_photos)


@app.route('/gallery')
def gallery():
    photos = GalleryPhoto.query.all()
    liked_photo_ids = [like.photo_id for like in current_user.likes] if current_user.is_authenticated else []
    return render_template('gallery.html', photos=photos, liked_photo_ids=liked_photo_ids)


@app.route('/reservations', methods=['GET', 'POST'])
@login_required
def reservations():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        guests = int(request.form.get('guests', 2))
        table_type = request.form.get('table_type', 'Standard Table')

        if not date or not time:
            flash('Please select both a date and seating time for your reservation.', 'error')
            return redirect(url_for('reservations'))

        new_res = Reservation(
            user_id=current_user.id,
            date=date,
            time=time,
            guests=guests,
            table_type=table_type,
            status='CONFIRMED'
        )
        db.session.add(new_res)
        db.session.commit()
        flash(f'Table reserved successfully for {guests} guests on {date} at {time}!', 'success')
        return redirect(url_for('reservations'))

    user_reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.created_at.desc()).all()
    return render_template('reservations.html', reservations=user_reservations)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Please provide your name, email, and message content.', 'error')
            return redirect(url_for('contact'))

        msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent to the Concierge. We will be in touch shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard') if current_user.is_admin else url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password')

        if action == 'login':
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash(f'Welcome to Lumière, {user.name}!', 'success')
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('admin_dashboard') if user.is_admin else url_for('home'))
            flash('Invalid email address or password. Please verify and try again.', 'error')

        elif action == 'register':
            name = (request.form.get('name') or '').strip()
            if not name or not email or not password:
                flash('All fields are required to create an account.', 'error')
            elif User.query.filter_by(email=email).first():
                flash('An account with this email address already exists. Please sign in.', 'error')
            else:
                new_user = User(
                    name=name,
                    email=email,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                flash('Account created successfully! Welcome to Lumière.', 'success')
                return redirect(url_for('home'))

    return render_template('auth.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('home'))
    return render_template(
        'admin.html',
        reservations=Reservation.query.order_by(Reservation.created_at.desc()).all(),
        menu_items=MenuItem.query.order_by(MenuItem.id.desc()).all(),
        messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    )


@app.route('/api/toggle-like/<int:photo_id>', methods=['POST'])
@login_required
def toggle_like(photo_id):
    existing = Like.query.filter_by(user_id=current_user.id, photo_id=photo_id).first()
    if existing:
        db.session.delete(existing)
        liked = False
    else:
        db.session.add(Like(user_id=current_user.id, photo_id=photo_id))
        liked = True
    db.session.commit()
    return jsonify({'success': True, 'liked': liked})


@app.route('/api/admin/menu/add', methods=['POST'])
@login_required
def add_menu_item():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    name = request.form.get('name')
    description = request.form.get('description')
    try:
        price = float(request.form.get('price', 0))
    except ValueError:
        price = 0.0
    category = request.form.get('category', 'mains')
    image_url = request.form.get('image_url')

    if name and description and image_url:
        new_item = MenuItem(
            name=name,
            description=description,
            price=price,
            category=category,
            image_url=image_url
        )
        db.session.add(new_item)
        db.session.commit()
        flash(f'Menu item "{name}" published successfully!', 'success')
    else:
        flash('Please fill in all menu item fields.', 'error')

    return redirect(url_for('admin_dashboard'))


@app.route('/api/admin/menu/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_menu_item(item_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Menu item "{item.name}" deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    print(f"Starting Lumière Restaurant server on http://127.0.0.1:5000 ...")
    app.run(debug=True, host='0.0.0.0', port=5000)