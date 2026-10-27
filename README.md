# Lumière Restaurant – Fine Dining Web Application

> **Modern Elegance. Timeless Flavor.**  
> An elevated, luxury culinary sanctuary web application built with Python Flask, TailwindCSS, and vanilla JavaScript.

---

## 🌟 Highlights & Features

- **Dining & Seasonal Menu**:
  - Interactive multi-category filter (*House Pastas, Grand Mains, Garden & Salads, Desserts, Wines & Cuvée*).
  - Auto-rotating featured chef's selection showcase.
  - Interactive heart-like favorites.
  - Persistent slide-out order cart drawer with local storage, real-time total, and item counter.

- **Table Reservation System**:
  - Full scheduling workflow with dining time slots, party sizes (1 to 8+ guests), and table atmosphere selection (*Main Dining Room, Window View, Tasting Counter, Intimate Velvet Booth, Terrace Veranda*).
  - Dual-panel guest view displaying **Upcoming Reservations** and **Past Dining History**.
  - Hospitality etiquette guidelines (sommelier consultation, dress code, grace period).

- **Executive Management Console (`/admin`)**:
  - Real-time KPI summary cards (Total Bookings, Menu Offerings, Customer Inquiries, Admin status).
  - Guest reservations roster with status indicators.
  - Dish catalog management with live deletion.
  - "Add New Menu Dish" modal connected to `/api/admin/menu/add`.
  - Customer inquiries inbox from the contact desk.

- **Guest Authentication**:
  - Tabbed portal for both **Sign In** and **Create Account**.
  - Secure session management powered by Flask-Login and Werkzeug password hashing.

- **Atmosphere & Visual Gallery**:
  - Interactive photo gallery featuring culinary art, the cellar, and dining spaces.
  - Heart-like toggles backed by database persistence.

- **Concierge Desk (`/contact`)**:
  - Direct inquiry form saving messages to the admin console.
  - Sanctuary address, telephone, email, and valet details.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+ / Flask 3.0
- **Database**: SQLite with Flask-SQLAlchemy 3.1 (automatic schema creation & seed data)
- **Authentication**: Flask-Login 0.6 & Werkzeug
- **Styling**: TailwindCSS (CDN), Google Fonts (*Playfair Display* & *Inter*), FontAwesome 6
- **Frontend Logic**: Vanilla JavaScript (ES6+), LocalStorage Cart

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/amadipromise16/Lumiere_restaurant.git
cd Lumiere_restaurant
```

### 2. Install Dependencies
```bash
py -m pip install -r requirements.txt
```

### 3. Launch the Application
```bash
py run.py
```

Open your browser to:
- **Local machine**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **On your phone / local network**: `http://<YOUR-LOCAL-IP>:5000`

---

## 🔑 Default Administrator Credentials

- **Email**: `centralpoppy@gmail.com`
- **Password**: `Amadipromise`
- **Admin Dashboard**: `http://127.0.0.1:5000/admin`

---

## 📁 Project Structure

```text
Lumiere_restaurant/
├── py/
│   └── app.py              # Main Flask application, models & routes
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Master layout with header, cart & footer
│   ├── home.html           # Landing page with hero & highlights
│   ├── menu.html           # Interactive menu & ordering drawer
│   ├── reservations.html   # Table reservations & history
│   ├── gallery.html        # Culinary photo gallery
│   ├── about.html          # Heritage, story & chef philosophy
│   ├── contact.html        # Concierge contact desk
│   ├── auth.html           # Sign In / Create Account portal
│   └── admin.html          # Executive management dashboard
├── static/
│   ├── css/style.css       # Custom luxury CSS styling & animations
│   └── js/main.js          # Cart, mobile nav, carousel & toasts
├── app.py                  # Entry point
├── run.py                  # Startup runner script
├── requirements.txt        # Python package dependencies
└── README.md               # Documentation
```

---

## 📄 License
MIT License. Crafted for Lumière Restaurant.
