from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"

# Book data structure (Linked List)
class Book:
    def __init__(self, isbn, title, author, copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies = copies
        self.next = None

class Library:
    def __init__(self):
        self.head = None

    def add_book(self, isbn, title, author, copies):
        new_book = Book(isbn, title, author, copies)
        if not self.head:
            self.head = new_book
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_book

    def search_book(self, isbn):
        current = self.head
        while current:
            if current.isbn == isbn:
                return current
            current = current.next
        return None

library = Library()

# Home Page
@app.route('/')
def index():
    current = library.head
    books = []
    while current:
        books.append(current)
        current = current.next
    return render_template('index.html', books=books)

# Add Book
@app.route('/add', methods=['POST'])
def add_book():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    copies = int(request.form['copies'])

    if library.search_book(isbn):
        flash('Book with this ISBN already exists.')
    else:
        library.add_book(isbn, title, author, copies)
        flash('Book added successfully!')
    
    return redirect(url_for('index'))

# Search Book
@app.route('/search', methods=['POST'])
def search_book():
    isbn = request.form['isbn']
    book = library.search_book(isbn)
    if book:
        return render_template('search_result.html', book=book)
    else:
        flash('Book not found!')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
