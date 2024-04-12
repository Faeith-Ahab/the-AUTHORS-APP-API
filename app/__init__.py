from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions import jwt,migrate,db,bcrypt
from flask_bcrypt import Bcrypt
from app.controllers.auth.books_controller import books
from app.controllers.auth.auth_controller import auth
from app.controllers.auth.companies_controller import company
 
def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    from app.models.users import User
    from app.models.books import Book
    from app.models.companies import Company
    
    
    @app.route("/")
    def home():
        return "AUTHORS API PROJECT"
    
    
    app.register_blueprint(books)
    app.register_blueprint(auth,url_prefix='/api/v1/auth')
    app.register_blueprint(company)
    
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

   