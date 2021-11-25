from datetime import datetime
from flasklib import db, login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship(
        'Role', 
        secondary=roles_users, 
        backref=db.backref('users', lazy='dynamic')
    )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self,name, **kwargs):
        return redirect(url_for('login'))


