from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime
from app.models.books import Book
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

# Define Blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')



# CREATE A BOOK

@books.route('/', methods=['POST'])
def create_book():
    try:
        # Extract data from request (using `get_json` for proper parsing)
        data = request.get_json()

        # Basic input validation
        required_fields = ['title', 'pages', 'price', 'price_unit', 'publication_date',
                           'isbn', 'genre', 'description', 'company_id', 'user_id']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "All required fields are missing"}), 400

        # Create a new book
        new_book = Book(
            title=data['title'],
            pages=data['pages'],
            price=data['price'],
            price_unit=data['price_unit'],
            publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date(),  # Parse date string
            isbn=data['isbn'],
            genre=data['genre'],
            description=data['description'],
            image=data['image'] if data.get('image') else None,  # Handle optional image
            company_id=data['company_id'],
            user_id=data['user_id']
        )

        # Add and commit to database
        db.session.add(new_book)
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Book '{new_book.title}' has been created"}), 201

    except Exception as e:
        # Handle exceptions appropriately (e.g., database errors, validation errors)
        return jsonify({"error": str(e)}), 500



# GET ALL BOOKS

@books.route('/', methods=['GET'])
def get_all_books():
    try:
        # Query all books
        books = Book.query.all()

        # Prepare response data
        book_data = [{
            "id": book.id,
            "title": book.title,
            "genre": book.genre,
            "publication_date": book.publication_date.strftime('%Y-%m-%d'),
            "isbn": book.isbn,
            "description": book.description,
            "company_id": book.company_id,
            "user_id": book.user_id
        } for book in books]

        return jsonify({"books": book_data}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
    

# GET A SPECIFIC BOOK

@books.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        # Query the book by id
        book = Book.query.get(book_id)

        # Check if the book exists
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Prepare response data
        book_data = {
            "id": book.id,
            "title": book.title,
            "genre": book.genre,
            "publication_date": book.publication_date.strftime('%Y-%m-%d'),
            "isbn": book.isbn,
            "description": book.description,
            "company_id": book.company_id,
            "user_id": book.user_id
        }

        return jsonify({"book": book_data}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



# UPDATE A BOOK

@books.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        # Extract data from request
        data = request.get_json()

        # Query the book by id
        book = Book.query.get(book_id)

        # Check if the book exists
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Update book attributes
        book.title = data.get('title', book.title)
        book.pages = data.get('pages', book.pages)
        book.price = data.get('price', book.price)
        book.price_unit = data.get('price_unit', book.price_unit)
        if 'publication_date' in data:
            book.publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d').date()
        book.isbn = data.get('isbn', book.isbn)
        book.genre = data.get('genre', book.genre)
        book.description = data.get('description', book.description)
        book.image = data.get('image', book.image)
        book.company_id = data.get('company_id', book.company_id)
        book.user_id = data.get('user_id', book.user_id)

        # Commit changes to database
        db.session.commit()

        return jsonify({"message": "Book updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
    

# DELETE A BOOK
@books.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Query the book by id
        book = Book.query.get(book_id)

        # Check if the book exists
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Delete the book
        db.session.delete(book)
        db.session.commit()

        return jsonify({"message": "Book deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
