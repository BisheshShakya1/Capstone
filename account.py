import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Secret key is required to use sessions securely
app.secret_key = 'super_secret_key_change_in_production' 

# --- Database Setup ---
def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- HTML Templates (For demonstration purposes) ---
REGISTER_HTML = '''
    <h2>Create Account</h2>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="/login">Login here</a></p>
'''

LOGIN_HTML = '''
    <h2>Login</h2>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/register">Register here</a></p>
'''

DASHBOARD_HTML = '''
    <h2>Welcome to your Dashboard!</h2>
    <p>Logged in as: {{ email }}</p>
    <a href="/logout">Logout</a>
'''

# --- Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Basic validation
        if not email or not password:
            return render_template_string(REGISTER_HTML, error="Email and password are required.")

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (email, password) VALUES (?, ?)', 
                (email, hashed_password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template_string(REGISTER_HTML, error="Email is already registered.")

    return render_template_string(REGISTER_HTML, error=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            # Store user info in session
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_HTML, error="Invalid email or password.")

    return render_template_string(LOGIN_HTML, error=None)


@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_HTML, email=session.get('email'))


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db() # Create the database table on startup
    app.run(debug=True)
