from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)


# creates database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creates an instance of database as db
db = SQLAlchemy(app)

# Create Table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html')

@app.route("/edit?=<book_id>", methods=["POST", "GET"])
def change_rating(book_id):
    book_to_update = Book.query.get(book_id)
    if request.method == "POST":
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update_rating.html", book=book_to_update)

@app.route("/delete<book_id>")
def delete_row(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


