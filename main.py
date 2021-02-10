from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviews.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template('index.html', books=Book.query.all())


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        book = Book(title=title, author=author, rating=rating)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_rating(book_id):
    book = Book.query.filter_by(id=book_id).first()
    print(book.rating)
    if request.method == 'POST':
        new_rating = request.form['new_rating']
        print(new_rating)
        book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_rating.html', book=book)


@app.route('/delete/<book_id>')
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

