import hashlib
import os

from flask import render_template, request, flash,send_from_directory, session
from flask import url_for, redirect

from app import app, db
from models import User, Product
from shop_functions import check_login
from datetime import timedelta
from config import Config

from werkzeug.utils import secure_filename


@app.route('/edit/<pid>', methods=['POST', 'GET'])
def edit_product(pid):
    profile = check_login()
    if profile is None:
        return redirect(url_for('login'))

    # check if product is in database
    pid = int(pid)
    product = Product.query.filter_by(id=pid).first()
    if product is None:
        flash("Article doesn't exist!")
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('edit.html', product=product)

    # Update product info
    product.title = request.form['title']
    product.category = request.form['category']
    product.description = request.form['description']
    

    db.session.commit()

    flash("{} updated successfully!".format(product.title))
    return redirect(url_for('dashboard'))

@app.route('/delete/<pid>')
def delete_product(pid):
    # check if porduct is in db
    pid = int(pid)
    product = Product.query.filter_by(id=pid).first()
    if product is None:
        flash("Article doesn't exist!")
        return redirect(url_for('dashboard'))

    db.session.delete(product)
    db.session.commit()
    flash("{} deleted successfully!".format(product.title))
    return redirect(url_for('dashboard'))
    

@app.route('/add_product', methods=['POST'])
def add_product():
    profile = check_login()
    if profile is None:
        return redirect(url_for('login'))
    # collect form data
    title = request.form['title']
    category = request.form['category']
    post = request.form['description']
    picture = request.files['picture']
    if title == '' or category == '' or post == '' or picture == '' or picture.filename == '':
        flash("All fields are required!")
        return redirect(url_for('add_product_page'))
    print("Uploading {}".format(picture.filename))
     # get name of picture
    filename = secure_filename(picture.filename)

    # save pictures
    picture.save(os.path.join(Config.UPLOADS_FOLDER, filename))
    # add form details to database
    product = Product(title=title, category=category, description=post, image=filename)

    db.session.add(product)
    db.session.commit()
    flash("{} posted successfully!".format(title))
    return redirect(url_for('dashboard'))
    


@app.route('/add_new_product')
def add_product_page():
    profile = check_login()
    if profile is None:
        return redirect(url_for('login'))
    return render_template("add_product.html")

    


@app.route('/dashboard')
def dashboard():
    profile = check_login()
    if profile is None:
        return redirect(url_for('login'))

    products = Product.query.all()
    return render_template("dashboard.html", profile=profile, products=products)

@app.route('/')
def homepage(): 
  
    return render_template("mira.html")


@app.route('/home')
def new():
    profile = check_login()
    products = Product.query.all()
    return render_template("Home.html", products=products, profile=profile)


@app.route('/post')
def post():
    profile = check_login()
    products = Product.query.all()
    return render_template("post.html", products=products, profile=profile)

@app.route('/login', methods=['GET', 'POST'])  
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if email == '' or password == '' or username == '':
            flash("All fields are required!")
            return render_template("login.html")
        p_hash = hashlib.sha256(password.encode()).hexdigest()
        # check if the user with email exist
        correct_user = User.query.filter_by(email=email).first()
        if correct_user is None:
            flash("Account doesn't exist")
            return render_template('login.html')

        if correct_user.password_hash == p_hash:
            flash("Successfully Logged In!",)
            session['email'] = email
            session['p_hash'] = p_hash
            # set cookies
            resp = redirect(url_for('collect'))
            resp.set_cookie('id', str(correct_user.id), max_age=timedelta(hours=24))
            resp.set_cookie('p_hash', p_hash, max_age=timedelta(hours=24))
            return resp
    flash("Invalid login details")
    return render_template('login.html')

@app.route('/logout')
def log_out():
    if 'email' in session:
        session.pop('email')
        session.pop('p_hash')
    # Remove cookies
    flash("You have successfully Logged out!")
    resp = redirect(url_for('login'))
    resp.set_cookie('id', expires=0)
    resp.set_cookie('p_hash', expires=0)
    return resp

@app.route('/collect')
def collect():
    profile = check_login()
    return render_template("collect.html", profile=profile)

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if username.isnumeric():
        flash("Enter letters only for username")
        return redirect(url_for('sign_up'))

    elif password == '' or email == '' or username == '':
        flash("All fields are required!")
        return redirect(url_for('sign_up'))
    else:
        p_hash = hashlib.sha256(password.encode()).hexdigest()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        new_user = User(username=username, email=email, password_hash=p_hash)
        db.session.add(new_user)
        db.session.commit()
        flash("Congrats! you now have a account idan.")
        return redirect(url_for('new'))
    else:
        flash("This email has been used by another user!")
        return redirect('sign_up')
        
            

@app.route('/uploads/<filename>')
def view_file(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/mira')
def mira():
    return render_template('mira.html') 
