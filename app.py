
from flask import Flask, render_template, request, redirect, url_for, session, flash
#from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.secret_key = 'kjdn983hdeidj09w3rhbg598hq2diwdjod9r6f6uuehudwiy4ygfyiro494jfjdshdir'  # Replace with a real secret key

# Initialize SQLAlchemy with your Flask app instance
db = SQLAlchemy(app)

# Import your models here
from models import User, Music

migrate = Migrate(app, db)

# Initialize Flask-Admin
admin = Admin(app, name='MyApp Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Music, db.session)) 

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  # Initialize an error message variable

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            error_message = 'Invalid username or password'  # Set the error message

    return render_template('login.html', error_message=error_message)





@app.route('/music')
def music():
    music_records = Music.query.all()
    return render_template('music.html', music_records=music_records)


@app.route('/add_to_profile/<int:music_id>', methods=['POST'])
def add_to_profile(music_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to add songs to your favorites.')
        return redirect(url_for('login'))

    # Retrieve the user and song
    user = User.query.get(session['user_id'])
    song = Music.query.get(music_id)

    # Add the song to the user's profile if not already added
    if song not in user.music:
        user.music.append(song)
        db.session.commit()
        flash('Song added to your favorites.')
    else:
        flash('Song already in your favorites.')

    # Redirect to the profile page
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/remove_from_profile/<int:music_id>', methods=['POST'])
def remove_from_profile(music_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to remove songs from your favorites.')
        return redirect(url_for('login'))

    # Retrieve the user and song
    user = User.query.get(session['user_id'])
    song = Music.query.get(music_id)

    # Remove the song from the user's profile if it exists
    if song in user.music:
        user.music.remove(song)
        db.session.commit()
        flash('Song removed from your favorites.')
    else:
        flash('Song not found in your favorites.')

    # Redirect to the profile page
    return redirect(url_for('profile'))




@app.route('/privacy_policy')
def privacy_policy():
    # Add your Privacy Policy content here
    return render_template('privacy_policy.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/artists')
def artists():
    return render_template('artists.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
