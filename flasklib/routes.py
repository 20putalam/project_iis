from flask import render_template, url_for, flash, redirect, request
from flasklib import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flasklib.models import User, Role, MyModelView, MyAdminIndexView, Library, Book
from flasklib.forms import ManageUsersForm, RegistrationForm, LoginForm, AddUsersForm, AddBook, RoleUserForm
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

@app.route("/knihy", methods=['GET', 'POST'])
def knihy():
    Books = Book.query
    form = AddBook()
    city_lib = Library.query.filter_by(city=form.library.data).first()
    if form.validate_on_submit():
        new_book = Book(name=form.name.data ,autor=form.autor.data ,publisher=form.publisher.data ,tag=form.tag.data ,all_books=city_lib)
        db.session.add(new_book)
        db.session.commit()   
        flash('Kniha byla přidána!', 'Úspěch')
    return render_template('knihy.html', title='Basic Table', Books=Books, form=form)

@app.route('/knihy_delete/<int:id>')
def knihy_delete(id):
    book_delete = Book.query.get_or_404(id)
    name = None
    form = AddBook()

    try:
        db.session.delete(book_delete)
        db.session.commit()
        flash("Kniha byla úspěšné smazána !")
        Books = Book.query
        return redirect(url_for('knihy'))
    except:
        flash("Při mazání nastala chyba !!")
        return redirect(url_for('knihy'))


@app.route("/manageusers")
def manageusers():

    form = RoleUserForm()
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin":

            users = User.query.order_by(User.id) 
            return render_template('manageusers.html', title='Admin Tools',users=users,form = form)

        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/user_delete/<int:id>')
def user_delete(id):

    try:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash("User byl úspěšné smazán !")
        return redirect(url_for('manageusers'))
    except:
        flash("Při mazání nastala chyba !!")
        return redirect(url_for('manageusers'))

@app.route('/user_update/<int:id>,<int:role>')
def user_update(id,role):

    try:
        User.query.filter_by(id=id).update(dict(role_id=role))
        db.session.commit()
        flash("User successfully updated !")
        return redirect(url_for('manageusers'))
    except:
        flash("Při mazání nastala chyba !!")
        return redirect(url_for('manageusers'))

@app.route("/addusers",methods=['GET', 'POST'])
def addusers():

    if  current_user.is_authenticated:
        if current_user.ro_user.name == "admin":

            form = AddUsersForm()

            if form.validate_on_submit():
                
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password=hashed_password, ro_user=Role.query.filter_by(name='reader').first())
                db.session.add(user)
                db.session.commit()
                flash('Učet byl vytvořen!', 'Úspěch')
                
            return render_template('addusers.html', title='Admin Tools',form=form)

        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
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
    return redirect(url_for('home'))
