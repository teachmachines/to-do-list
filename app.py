from flask import Flask, request, render_template, url_for, redirect, flash
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, ProgrammingError

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
    #  TODO: Add email validation for regex that has a minimum of 5 characters and a maximum of 255 characters
    #
    email = db.Column(db.String(255), nullable=False, unique=True)
    # TODO: Add email validation for regex that has a minimum of 5 characters and a maximum of 255 characters
    message = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'

    def __init__(self, name, email, message):
        if len(name) < 5:
            raise ValueError("Name must be at least 5 characters")
        elif len(name) > 30:
            raise ValueError("Name must be less than 30 characters")
        if len(email) < 5:
            raise ValueError("Email must be at least 5 characters")
        elif len(email) > 255:
            raise ValueError("Email must be less than 255 characters")
        if len(message) < 5:
            raise ValueError("Message must be at least 5 characters")
        elif len(message) > 255:
            raise ValueError("Message must be less than 255 characters")
        import re
        email_regex = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
        if not email_regex.match(email):
            raise ValueError("Email is not valid")
        name_regex = re.compile(r'^[a-zA-Z\s]+$')
        if not name_regex.match(name):
            raise ValueError("Name is not valid")

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
        try:
            new_contact = Contact(name, email, message)
        except ValueError as e:
            flash(e.args[0], 'danger')
            # Log the error
            logging.error(e)
            return render_template("contact.html")

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash(f'Thanks {name}, your message has been sent!', 'success')
            return render_template("contact.html")
        except OperationalError as e:
            flash(f'Unfortunately you message has not been received, please try again', 'danger')
            # Log the error
            logging.error(e)
            return render_template("contact.html")
        except DataError as e:
            flash(f'Unfortunately your message was not accepted by the database', 'danger')
            # Log the error
            logging.error(e)
            return render_template("contact.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        new_user = User(email, password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Thanks {email}, your account has been created!', 'success')
            return redirect(url_for("login"))
        except SQLAlchemy.exc.SQLAlchemyError as e:
            logging.error(e)
            flash(f'Unfortunately you account has not been created because the email is already registered', 'danger')
            return render_template("register.html")

    return render_template("register.html")


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
