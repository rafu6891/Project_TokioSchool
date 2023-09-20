"""
Flask Application: Gaming User Management.
This application provides user authentication, profile management and game activity tracking.
It includes administrative functions for user management and game metrics visualization.
"""


from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User
import db
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = '987654321'
admin_password = '987654321'  # Definir la contraseña de administrador


@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registratiion. Validates input and creates a new user."""
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        is_admin = 'is_admin' in request.form
        admin_password = request.form.get('admin_password')

        existing_user = User.custom_query().filter_by(name=name).first()
        if existing_user is not None:
            flash('Ya existe un usuario con ese nombre.')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.')
            return redirect(url_for('signup'))

        password = generate_password_hash(password)

        if is_admin and admin_password != admin_password:
            return 'Contraseña de administrador incorrecta.'

        nuevo_usuario = User(name=name, password=password, email=email, is_admin=is_admin)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login. Validates credentials and manages user session."""
    error_message = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = db.session.query(User).filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            if user.is_admin:
                return redirect('/admin/users')
            else:
                return redirect('/profile')
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos.'
    return render_template('login.html', error_message=error_message)

def login_required(f):
    """Decorator to ensure the user is logged in before accessing certain routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to ensure the user has admin rights before accessing certain routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect('/login')
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user.is_admin:
            return 'No tienes permiso para acceder a esta página.'
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/users')
@admin_required
def admin_users():
    """List all user for the admin."""
    users = db.session.query(User).all()
    return render_template('admin/users.html', users=users)

@app.route('/profile')
@login_required
def profile():
    """Display the profile of the logged-in user with game statistics."""
    user_id = session['user_id']
    user = db.session.query(User).filter_by(id=user_id).first()

    total_games = user.tetris_count + user.cod_count
    tetris_percentage = 0 if total_games == 0 else (user.tetris_count / total_games) * 100
    cod_percentage = 0 if total_games == 0 else (user.cod_count / total_games) * 100

    return render_template('profile.html', user=user, tetris_percentage=tetris_percentage, cod_percentage=cod_percentage)

@app.route('/admin/users/rank', methods=['GET'])
@login_required
def admin_users_rank():
    """List all users for the admin to modify rankings."""
    if not session.get('is_admin'):
        return "Acceso no autorizado", 403
    users = User.custom_query().all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>/rank', methods=['POST'])
@login_required
def rank_user(user_id):
    """Adjust the ranking of a specific user by the admin."""
    if not session.get('is_admin'):
        return "Acceso no autorizado", 403
    user = User.custom_query().get(user_id)
    operation = request.form.get('operation')
    if operation == 'increment':
        user.ranking += 1
    elif operation == 'decrement':
        user.ranking -= 1
    db.session.commit()
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Allow the admin to delete a specific user."""
    if not session.get('is_admin'):
        return "Acceso no autorizado", 403
    user = User.custom_query().get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_users'))


@app.route('/game_played/<game_name>', methods=['POST'])
@login_required
def game_played(game_name):
    """Track a played game for the logged-in user and update their stats."""
    if game_name not in ['tetris', 'cod']:
        return 'Juego desconocido', 400

    user_id = session.get('user_id')
    if user_id is None:
        return 'Usuario no autenticado', 400

    user = User.custom_query().get(user_id)

    if game_name == 'tetris':
        user.tetris_count += 1
    elif game_name == 'cod':
        user.cod_count += 1
    db.session.commit()
    return redirect(url_for('profile'))


if __name__ == '__main__':
    """Create a predefined administrator user at the start of the application if it does not exist."""
    db.Base.metadata.create_all(db.engine)
    admin = db.session.query(User).filter_by(name='admin').first()
    if admin is None:
        admin = User(name='admin', password=generate_password_hash(admin_password), email='admin@example.com', is_admin=True)
        db.session.add(admin)
        db.session.commit()
    app.run(debug=True)