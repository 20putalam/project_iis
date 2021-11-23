from flask import render_template, url_for, flash, redirect, request
from flasklib import app, db, bcrypt


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

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')