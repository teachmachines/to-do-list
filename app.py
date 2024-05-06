from flask import Flask, request, render_template, url_for, redirect, flash
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import logging

# Create the Web Server Gateway Interface Application
# __name__ returns the file name e.g. app.py this lets us know where to find things like the template
app = Flask(__name__)
#  Flask is a configuration object used to store the configuration parameters of a Flask application
# Here we specify where the database will be stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
#  SQLAlchemy will not signal the application every time a change is about to be made in the database.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# The secret key is used to secure the session data stored in the cookies.
app.config['SECRET_KEY'] = 'your-unique-secret-key'

# Create a database object
db = SQLAlchemy(app)


class User(db.Model):
    """Create a User class that inherits from db.Model. This class will be used to create the database table.
    The class has three columns: id, username, and password. The id column is the primary key, username is a
    unique string, and password is a string."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def check_login(username: str, password: str):
        """Check if the username and password are valid."""
        return bool(User.query.filter_by(username=username, password=password).first())


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message


# Create the database
with app.app_context():
    db.create_all()

# Set up logging
logging.basicConfig(filename='app.log',
                    filemode='w',  # Overwrites the log file
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        new_contact = Contact(name, email, message)
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash(f'Thanks {name}, your message has been sent!', 'success')
            return render_template("contact.html")
        except SQLAlchemy.SQLAlchemyError as e:
            flash(f'Unfortunately you message has not been received, please try again', 'danger')
            # Log the error
            logging.error(e)
            return render_template("contact.html")


@app.route("/hello_world")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {username}'


@app.route('/todo/<int:todo_id>')
def show_post(todo_id):
    # show the post with the given id, the id is an integer
    return f'Todo {todo_id}'


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.check_login(username, password)
        if user:
            return redirect(url_for("index"))
        else:
            error = "Login Attempt Failed"
            return render_template("login.html", error=error)
    elif request.method == "GET":
        return render_template("login.html", error=error)


if __name__ == '__main__':
    app.run()
