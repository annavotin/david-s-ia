from flask import Blueprint, Flask, redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from .models import *
from passlib.hash import pbkdf2_sha256 as hasher
from os import path
from functools import wraps
from website.models import *
from . import db


views = Blueprint('views', __name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'id' in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return wrap


@views.route("/home/<index>", methods = ["GET", "POST"])
@login_required
def home(index):
    student = Students.query.filter_by(id=session['id']).first()
    books = Books.query.filter_by(student_id = session["id"], status="reading").order_by(desc(Books.book_id)).all()
    
    if request.method == 'POST':
        index = request.form["next_book"]
        if int(index) >= len(books):
            index = 0
   
    return render_template("home.html", student=student, books=books, index=index)


@views.route("/list", methods = ["GET", "POST"])
@login_required
def list():
    student = Students.query.filter_by(id=session['id']).first()
    books = Books.query.filter_by(student_id = session["id"]).order_by(Books.status).all()
    if request.method=='POST' and request.form['button'][:4] == "more":
        return redirect(url_for('views.detail', book_id=request.form['button'][4:]))
    return render_template("list.html", student=student, books=books)


@views.route("/add", methods = ["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        name = request.form["name"]
        author = request.form["author"]
        total_pages = (request.form["no_pages"])
        current_page = (request.form["current_page"])
        
        f = request.files['file']
        try:
            f.save("davids-ia/website/static/images/" + name.replace(" ", "_"))
        except:
            f.filename = "batman.png"
        book = Books(student_id = session["id"], name = name, author = author, pages = total_pages, bookcover = "davids-ia/website/static/images/" + str(f.filename), currentpage = current_page, status="reading")
        db.session.add(book)
        db.session.commit()
        flash("Book successfully added!")
        
        return redirect(url_for('views.list'))
    
    
@views.route("/goal", methods = ["GET", "POST"])
@login_required
def goal():
    if request.method == "GET":
        goals = Goals.query.filter_by(student_id=session["id"])
        goal_array = []
        for i in goals:
            goal_array.append(i)
        return render_template("goal.html", goals=goal_array)
    else:
        value = request.form["button"]
    
    #Save
        if value == "save":
            new_goal = Goals(student_id=session["id"], goal=request.form.get("title"), checked=False)
            db.session.add(new_goal)
            db.session.commit()
    #Delete
        elif value[:3] == "del":
            deleted = Goals.query.filter_by(id=value[3:]).first()
            db.session.delete(deleted)
            db.session.commit()
    #Checkbox
        else:
            goal = Goals.query.get(value[5:])
            if goal:
                goal.checked = not goal.checked
                db.session.add(goal)
                db.session.commit()
            
        return redirect("/goal")
    
@views.route("/detail/<book_id>", methods=["GET", "POST"])
@login_required
def detail(book_id):
    if request.method=='POST': book_id = request.form['button']
    book = Books.query.filter_by(book_id=book_id).first()
    if not book:
        flash("Book not found", category="error")
    elif request.method == 'POST':
        print("ID" + str(book_id))
        name=book.name
        author=book.author
        pages=book.pages
        current_page=book.currentpage
        file_name=book.bookcover
        status = request.form['book_status']
        
        if request.form['name'] != "": name = request.form["name"]
        if request.form['author'] != "": author = request.form["author"]
        if request.form['no_pages'] != "": pages = (request.form["no_pages"])
        if request.form['current_page'] != "": current_page = (request.form["current_page"])
        if request.files['file']: file_name="davids-ia/website/static/images/static" + str(request.files['file'].name)
        flash(str(request.files['file'].name))
        
        new_book = Books(student_id = session["id"], name = name, author = author, pages = pages, bookcover = file_name, currentpage = current_page, status=status)
        db.session.add(new_book)
        db.session.delete(book)
        db.session.commit()
        flash("Book successfully added!")
        
        return redirect(url_for('views.list'))
    
    return render_template("detail.html", book=book)
        
@views.route("/challenge", methods=["GET", "POST"])
@login_required
def challenge():
    challenges = Challenges.query.all()
    return render_template("challenge.html", challenges=challenges)