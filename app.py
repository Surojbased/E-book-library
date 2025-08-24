from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash
from models import db, User
from form import LoginForm

# ------------------------
# App Configuration
# ------------------------
app = Flask(__name__, static_folder='static')
app.secret_key = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ebook_library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

# ------------------------
# Google OAuth Setup
# ------------------------
google_bp = make_google_blueprint(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    scope=["profile", "email"],
    redirect_to="google_authorized"
)
app.register_blueprint(google_bp, url_prefix="/login")


# ------------------------
# Authentication Routes
# ------------------------
@app.route("/google-login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    info = resp.json()
    # store info['email'], etc.
    return redirect(url_for("dashboard"))


@app.route('/add-test-user')
def add_test_user():
    password = generate_password_hash("123456").decode("utf-8")
    user = User(email="subhamdebnath129@gmail.com", password=password)
    db.session.add(user)
    db.session.commit()
    return "Test user created!"


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Inline password validation
        def isvalid(passw):
            if 8 <= len(passw) <= 16:
                if passw != passw.lower() and passw != passw.upper():
                    if not passw.isalnum():
                        for i in range(10):
                            if str(i) in passw:
                                return "OK"
                        flash("At least 1 digit required", "error")
                    else:
                        flash("Special character missing", "error")
                else:
                    flash("At least 1 uppercase and 1 lowercase required", "error")
            else:
                flash("Password must be 8–16 characters long", "error")
            return "INVALID"

        if isvalid(password) != "OK":
            return render_template('dashboard.html', form=form)

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "error")

    return render_template('login.html', form=form)


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    conpass = request.form.get('conpass')

    if password != conpass:
        flash("Passwords do not match.", "danger")
        return redirect(url_for('login'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists. Please log in.", "warning")
        return redirect(url_for('login'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! Please log in.", "success")
    return redirect(url_for('login'))


@app.route('/logout.html')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return render_template('logout.html', form=LoginForm())


# ------------------------
# Static Pages
# ------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard.html')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/analytics.html')
def analytics():
    return render_template('analytics.html')


@app.route('/author.html')
def author():
    return render_template('author.html')


@app.route('/authors.html')
def authors():
    return render_template('authors.html')


@app.route('/books.html')
def books():
    return render_template('books.html')


@app.route('/Categories.html')
def categories():
    return render_template('Categories.html')


@app.route('/profile.html')
def profile():
    return render_template('profile.html')


@app.route('/readmore.html')
def readmore():
    return render_template('readmore.html')


@app.route('/settings.html')
def settings():
    return render_template('settings.html')


@app.route('/user/<username>')
def show_user(username):
    return f'Hello {username}!'


@app.route('/hello')
def hello():
    return "Hello, Welcome to GeeksForGeeks"


# ------------------------
# API Routes
# ------------------------
@app.route("/profile")
def get_profile():
    # Example static data — replace with DB fetch if needed
    profile_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@bookdashboard.com",
        "phone": "+1 (555) 123-4567",
        "department": "Information Technology",
        "position": "System Administrator",
        "bio": "Experienced system administrator with over 8 years...",
        "stats": {
            "books_added": 156,
            "authors": 42,
            "reviews": 89
        },
        "badges": ["Admin", "Verified", "Premium"],
        "activity": [
            {
                "icon": "book",
                "color": "primary",
                "title": 'Added new book "The Digital Revolution"',
                "desc": "Added a new science fiction novel to the collection",
                "time": "2 hours ago"
            },
            {
                "icon": "user-plus",
                "color": "success",
                "title": "New author registered",
                "desc": "Sarah Mitchell joined as a new author",
                "time": "5 hours ago"
            }
        ],
        "security": {
            "two_factor": "Enabled",
            "password_last_changed": "30 days ago",
            "login_notifications": "Email & SMS",
            "last_login": "Today at 9:15 AM"
        }
    }
    return jsonify(profile.html)


# ------------------------
# DB Initialization
# ------------------------
def init_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
