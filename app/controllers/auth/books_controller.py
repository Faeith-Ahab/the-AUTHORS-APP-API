from flask import Blueprint, request, jsonify

from app.models.books import Book

from app.extensions import db
from datetime import datetime

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
        required_fields = ['title', 'pages', 'price', 'currency', 'publication_date',
                           'isbn', 'genre', 'description', 'company_id', 'user_id']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "All fields are REQUIRED"}), 400

        # Create a new book
        new_book = Book(
            title=data['title'],
            pages=data['pages'],
            price=data['price'],
            currency=data['currency'],
            publication_date=['publication_date'], 
            isbn=data['isbn'],
            genre=data['genre'],
            description=data['description'],
            image=data['image'] if data.get('image') else None,  # Handle optional image
            user_id=data['user_id'],
            company_id=data['company_id']
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
            "pages": book.pages,
            "price": book.price,
            "currency": book.currency,
            "publication_date": book.publication_date,
            "isbn": book.isbn,
            "genre": book.genre,
            "description": book.description,
            "image": book.image,
            "user_id": book.user_id,
            "company_id": book.company_id
            
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
            "pages": book.pages,
            "price": book.price,
            "currency": book.currency,
            "genre": book.genre,
            "publication_date": book.publication_date,
            "isbn": book.isbn,
            "genre": book.genre,
            "description": book.description,
            "image": book.image,
            "user_id": book.user_id,
            "company_id": book.company_id
            
        }

        return jsonify({"book": book_data}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



# UPDATE A BOOK


@books.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        # Get book object by ID
        book = Book.query.get(book_id)

        # Check if book exists
        if not book:
            return jsonify({"error": f"Book with ID {book_id} not found"}), 404

        # Extract data from request (excluding ID)
        data = request.json
        update_data = {field: data.get(field) for field in ['title', 'pages', 'price', 'currency', 'publication_date', 'isbn', 'genre', 'description', 'image', 'user_id', 'company_id'] if field != 'id'}

        # Update book attributes
        for field, value in update_data.items():
            setattr(book, field, value)

        # Commit changes to database
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Book with ID {book_id} has been updated"}), 200

    except Exception as e:
        # Handle exceptions appropriately
        return jsonify({"error": str(e)}), 500



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
