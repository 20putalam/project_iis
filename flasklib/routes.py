from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from flasklib import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flasklib.models import Order, User, Role, MyModelView, MyAdminIndexView, Library, Book, Reservation, Borrowing, Votes
from flasklib.forms import AddLibrariesForm, ChangeLibrariesForm, OrderBookForm, RegistrationForm, LoginForm, AddUsersForm, AddBook
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Library, db.session))
admin.add_view(MyModelView(Book, db.session))
admin.add_view(MyModelView(Votes, db.session))
admin.add_view(MyModelView(Order, db.session))
admin.add_view(MyModelView(Borrowing, db.session))
admin.add_view(MyModelView(Reservation, db.session))

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')
#<!--<a href="{{ url_for('user_self_update', id=user.id)}}"> <button type="button" class="btn btn-secondary">Update</button> </a>-->
@app.route("/account")
def account():
    if current_user.is_authenticated:
        reservations = Reservation.query.filter_by(user_id=current_user.id)
        borrowings = Borrowing.query.filter_by(user_id=current_user.id)
        return render_template('account.html',user=current_user,reservations=reservations,borrowings=borrowings)   
    else:
        return redirect(url_for('login'))

@app.route("/books")
def books():
    books = Book.query.order_by(Book.id)
    return render_template('books.html',books=books)

@app.route("/librarian")
def librarian():
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin":
            reservations = Reservation.query.all()
            borrowings = Borrowing.query.all()
            return render_template('librarian.html',reservations=reservations,borrowings=borrowings)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    

@app.route("/confirm_borrowing/<int:res_id>/<int:id_user>/<int:id_book>")
def confirm_borrowing(res_id,id_user,id_book):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
            try:
                Reservation.query.filter_by(id=res_id).delete()
                borrowing = Borrowing(user_id=id_user, book_id=id_book)
                db.session.add(borrowing)
                db.session.commit()
                flash("User borrowed book successfully!")
                return redirect(url_for('librarian'))
            except:
                flash("Error!")
                return redirect(url_for('librarian'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route("/books_reserve/<int:id>")
def book_reserve(id):
    if current_user.is_authenticated:
        try:
            book = Book.query.filter_by(id=id).first()
            if book.number_of == 0:
                flash("No more copies left!")
                return redirect(url_for('books'))
            else:
                book.number_of-=1
                reservation = Reservation(user_id=current_user.id, book_id=id)
                db.session.add(reservation)
                db.session.commit()
                flash("Book reserved successfully!")
                return redirect(url_for('books'))
        except:
            flash("Error!")
            return redirect(url_for('books'))
    else:
        return redirect(url_for('login'))

@app.route("/delete_reservation/<int:res_id>")
def delete_reservation(res_id):
    if current_user.is_authenticated:
        try:
            reservation = Reservation.query.filter_by(id=res_id).first()
            book = Book.query.filter_by(id=reservation.book_id).first()
            book.number_of+=1
            Reservation.query.filter_by(id=res_id).delete()
            db.session.commit()
            flash("Reservation deleted successfully!")
            if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
                return redirect(url_for('librarian'))
            else:
                return redirect(url_for('account'))
        except:
            flash("Error!")
            if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
                return redirect(url_for('librarian'))
            else:
                return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

@app.route("/delete_borrowing/<int:bor_id>")
def delete_borrowing(bor_id):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
            try:
                borrowing = Borrowing.query.filter_by(id=bor_id).first()
                try:
                    book = Book.query.filter_by(id=borrowing.book_id).first()
                    book.number_of+=1
                except:
                    flash("Book is no longer offered!")
                Borrowing.query.filter_by(id=bor_id).delete()
                db.session.commit()
                flash("Book returned successfully!")
                return redirect(url_for('librarian'))
            except:
                flash("Error!")
                return redirect(url_for('librarian'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route("/libraries")
def libraries():
    libraries = Library.query.order_by(Library.id)
    return render_template('libraries.html',libraries=libraries)

@app.route("/managebooks", methods=['GET', 'POST'])
def managebooks():
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian" or current_user.ro_user.name == "distributor":
            Books = Book.query
            form = AddBook()
            form.library.choices = form.fill_choices()
            if form.validate_on_submit():
                
                lib_city=form.library.data
                lib_city = Library.query.get_or_404(lib_city)

                new_book = Book(name=form.name.data ,autor=form.autor.data ,publisher=form.publisher.data ,tag=form.tag.data, number_of=form.number_of.data,all_books=lib_city, img=form.img.data)
                db.session.add(new_book)
                db.session.commit()   
                flash('Book added successfully!', 'Success')
            return render_template('managebooks.html', title='Basic Table', Books=Books, form=form)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route("/orderbooks", methods=['GET', 'POST'])
def orderbooks():
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
            form = OrderBookForm()
            orders = Order.query
            if form.validate_on_submit():
                new_order = Order(book_id=form.id.data,number_of=form.number_of.data)
                db.session.add(new_order)
                db.session.commit()   
                flash('Book ordered successfully!', 'Success')
            return render_template('orderbooks.html', title='Basic Table', orders=orders, form=form)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    
@app.route("/supplybooks", methods=['GET', 'POST'])
def supplybooks():
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin"  or current_user.ro_user.name == "distributor":
            orders = Order.query.order_by(Order.id.desc())
            return render_template('supplybooks.html',orders=orders)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route("/supply/<int:order_id>/<int:book_id>/<int:amount>")
def supply(order_id,book_id,amount):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin"  or current_user.ro_user.name == "distributor":
            
            book = Book.query.get_or_404(book_id)
            book.number_of += amount
            Order.query.filter_by(id = order_id).delete()
            db.session.commit()
            flash("Books supplied successfully!")
            return redirect(url_for('supplybooks'))
        
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/book_delete/<int:id>')
def book_delete(id):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian" or current_user.ro_user.name == "distributor":
            book_delete = Book.query.get_or_404(id)
            try:
                Reservation.query.filter_by(book_id=id).delete()
                db.session.delete(book_delete)
                db.session.commit()
                flash("Book deleted successfully!")
                return redirect(url_for('managebooks'))
            except:
                flash("Error!")
                return redirect(url_for('managebooks'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/book_update<int:id>', methods=['GET', 'POST'])
def book_update(id):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian" or current_user.ro_user.name == "distributor":
            form = AddBook()
            book_update = Book.query.get_or_404(id)
            if form.validate_on_submit():
                book_update.name = form.name.data
                book_update.autor = form.autor.data
                book_update.publisher = form.publisher.data
                book_update.tag = form.tag.data
                book_update.number_of = form.number_of.data
                book_update.img = form.img.data
                
                lib_city=form.library.data
                lib_city = Library.query.get_or_404(lib_city)
                book_update.all_books = lib_city

                db.session.commit()
                flash("Book updated successfully!")
                return redirect(url_for('managebooks'))
            else:   
                return render_template("update_book.html", form=form, book_update = book_update)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    
@app.route("/manageusers",methods=['GET', 'POST'])
def manageusers():

    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin":

            users = User.query.order_by(User.id) 
            return render_template('manageusers.html', title='Admin Tools',users=users)

        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/user_delete/<int:id>')
def user_delete(id):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin":
            try:
                User.query.filter_by(id=id).delete()
                db.session.commit()
                flash("User deleted successfully!")
                return redirect(url_for('manageusers'))
            except:
                flash("Error!")
                return redirect(url_for('manageusers'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/user_update/<int:id>/<int:role>')
def user_update(id,role):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin":

            try:
                User.query.filter_by(id=id).update(dict(role_id=role))
                db.session.commit()
                flash("User updated successfully!")
                return redirect(url_for('manageusers'))
            except:
                flash("Error!")
                return redirect(url_for('manageusers'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

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
                flash('Account created successfully!', 'Success')
                
            return render_template('addusers.html', title='Admin Tools',form=form)

        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

############################################################################################################################################

@app.route("/managelibraries",methods=['GET', 'POST'])
def managelibraries():

    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
            libraries = Library.query.order_by(Library.id)
            form1 = AddLibrariesForm()
            form2 = ChangeLibrariesForm()
            if form1.validate_on_submit():
                if form1.submit_add.data:
                    
                    par1 = Library.query.filter_by(city=form1.city.data).first()
                    par2 = Library.query.filter_by(street=form1.street.data).first()
                    par3 = Library.query.filter_by(housenumber=form1.housenumber.data).first()
                    if par1 and par2 and par3:
                        flash("Library already exists!")
                        return redirect(url_for('managelibraries'))

                    library = Library(city=form1.city.data, street=form1.street.data, housenumber=form1.housenumber.data)
                    db.session.add(library)
                    db.session.commit()
                    flash('Library created successfully!', 'Success')

            if form2.validate_on_submit():
                if form2.submit_change.data:

                    par1 = Library.query.filter_by(city=form2.city.data).first()
                    par2 = Library.query.filter_by(street=form2.street.data).first()
                    par3 = Library.query.filter_by(housenumber=form2.housenumber.data).first()
                    if par1 and par2 and par3:
                        flash("Library already exists!")
                        return redirect(url_for('managelibraries'))

                    try:
                        Library.query.filter_by(id=form2.id.data).update(dict(city=form2.city.data))
                        Library.query.filter_by(id=form2.id.data).update(dict(street=form2.street.data))
                        Library.query.filter_by(id=form2.id.data).update(dict(housenumber=form2.housenumber.data))
                        db.session.commit()
                    except:
                        flash("Library ID to update not found!")


            return render_template('managelibraries.html', title='Admin Tools',libraries = libraries,form1=form1,form2=form2)

        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/library_delete/<int:id>')
def library_delete(id):
    if current_user.is_authenticated:
        if current_user.ro_user.name == "admin" or current_user.ro_user.name == "librarian":
            try:
                Library.query.filter_by(id=id).delete()
                db.session.commit()
                flash("Library deleted successfully!")
                return redirect(url_for('managelibraries'))
            except:
                flash("Error!")
                return redirect(url_for('managelibraries'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
############################################################################################################################################


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
            flash('Login unsuccessfull! Check password and mail address', 'Error')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.username.data == "admin":
            role = 'admin'
            role1 = Role(name='admin', description='all perms')
            role2 = Role(name='reader', description='reader')
            role3 = Role(name='librarian', description='librarian')
            role4 = Role(name='distributor', description='distributor')
            db.session.add(role1)
            db.session.add(role2)
            db.session.add(role3)
            db.session.add(role4)
            db.session.commit()
        else:
            role = 'reader'
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, ro_user=Role.query.filter_by(name=role).first())
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can log in now', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
