from flask import Flask
from markupsafe import escape

# Create the Web Server Gateway Interface Application
# __name__ returns the file name e.g. app.py this lets us know where to find things like the template
app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return 'Hello World!'


@app.route("/hello_world")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:sub-path>')
def show_sub_path(sub_path):
    # show the sub-path after /path/
    return f'Sub-path {escape(sub_path)}'


# This route will allow you to also access /projects
@app.route('/projects/')
def projects():
    return 'The project page'


# This route will not allow you to access /about/
@app.route('/about')
def about():
    return 'The about page'


if __name__ == '__main__':
    app.run()
