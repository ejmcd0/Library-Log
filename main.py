from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

# all_books = []

class Book(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author:Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars().all()
    return render_template('index.html', book_list=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )

        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit', methods=['POST', 'GET'])
def edit_rating():
    if request.method == 'POST':
        book_id = request.form["id"]
        rating_to_edit = db.get_or_404(Book, book_id)
        # rating_to_edit = db.session.execute(db.select(Book).where(Book.id == num)).scalar()
        # current_book = rating_to_edit.title
        # current_rating = rating_to_edit.rating
        #new_rating = request.form["new_rating"]
        rating_to_edit.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template('rating.html', book=book_selected)

@app.route('/delete')
def delete():
    book_id = request.args.get("id")
    delete_book = db.get_or_404(Book, book_id)
    # num = Book.id
    # delete_book = db.session.execute(db.select(Book).where(Book.id == num)).scalar()
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for('home'))
    #return render_template('index.html', num=Book.id)


if __name__ == "__main__":
    app.run(debug=True)

