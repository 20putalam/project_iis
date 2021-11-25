from flask import render_template, url_for, flash, redirect, request
from flasklib import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flasklib.models import User, Role, MyModelView, MyAdminIndexView, Library, Book
from flasklib.forms import RegistrationForm, LoginForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Library, db.session))
admin.add_view(MyModelView(Book, db.session))


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

@app.route("/knihovny")
def knihovny():
    return render_template('knihovny.html')

@app.route("/knihy")
def knihy():
    return render_template('knihy.html')

@app.route("/myAdmin")
def knihy():
    return render_template('myAdmin.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Příhlašení neúspěsné! Zkontrolujte heslo a email', 'chyba')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, ro_user=Role.query.filter_by(name='reader').first())
        db.session.add(user)
        db.session.commit()
        flash('Váš učet byl vytvořen! Nyní se můžete  přihlásit', 'Úspěch')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return render_template('index.html')
