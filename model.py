class User(db.Model):
    """Create a User class that inherits from db.Model. This class will be used to create the database table.
    The class has three columns: id, username, and password. The id column is the primary key, username is a
    unique string, and password is a string."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'