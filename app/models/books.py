from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  
    currency = db.Column(db.String(50), nullable=False, default='UGX')
    publication_date = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(30), nullable=True, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)  
    user = db.relationship('User', backref='books')
    company = db.relationship('Company', backref='books')

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, title, pages, price, currency, publication_date, genre, description, user_id, company_id, isbn=None, image=None):
        self.title = title
        self.pages = pages
        self.price = price
        self.currency = currency
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.image = image
        self.user_id = user_id
        self.company_id = company_id

    def get_full_name(self):
        return self.title




# from app.extensions import db ##,bcrypt

# from datetime import datetime

# class Book(db.Model):
#     __tablename__ = "books"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), nullable=False)
#     pages = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)  
#     currency = db.Column(db.String(50), nullable=False, default='UGX')
#     publication_date = db.Column(db.String(50), nullable=False)
#     isbn = db.Column(db.String(30), nullable=True, unique=True)
#     genre = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(255), nullable=False)
#     image = db.Column(db.String(255), nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  
#     company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)  
#     user = db.relationship('User', backref='books')
#     company = db.relationship('Company', backref='books')

#     created_at = db.Column(db.DateTime, default=datetime.now())
#     updated_at = db.Column(db.DateTime, onupdate=datetime.now())

#     def __init__(self, title, pages, price, currency, publication_date,  genre, description, user_id, company_id,  isbn=None, image=None):
#         super(Book, self).__init__()
#         self.title = title
#         self.pages = pages
#         self.price = price
#         self.currency = currency
#         self.publication_date = publication_date
#         self.isbn = isbn
#         self.genre = genre
#         self.description = description
#         self.image = image
#         self.user_id = user_id
#         self.company_id = company_id
        

#     def get_full_name(self):
#         return self.title