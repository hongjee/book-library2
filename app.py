from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ondemand@localhost:5432/book_library_db'  

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(10), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()  # Create the database tables if they don't exist


def add_book(title, author, published_date, isbn):
    new_book = Book(title=title, author=author, published_date=published_date, isbn=isbn)
    db.session.add(new_book)
    db.session.commit()
    

def get_books():
    return Book.query.all()


@app.route('/', methods=['GET'])
def list_books():
    books = get_books()
    return '<br>'.join([f'{book.title} by {book.author} ({book.published_date}) - ISBN: {book.isbn}' for book in books])


if __name__ == '__main__':
    app.run(debug=True)

