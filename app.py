from flask import Flask, request, render_template, url_for, redirect
from markupsafe import escape
import db

# Create the Web Server Gateway Interface Application
# __name__ returns the file name e.g. app.py this lets us know where to find things like the template
app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


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


# This route will not allow you to access /about/
@app.route('/about')
def about():
    return 'The about page'


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.valid_login(username, password):
            return redirect(url_for("index"))
        else:
            error = "Login Attempt Failed"
            return render_template("login.html", error=error)
    elif request.method == "GET":
        return render_template("login.html", error=error)





if __name__ == '__main__':
    app.run()
