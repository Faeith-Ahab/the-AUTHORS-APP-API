# Application factory function

from flask import Flask

from extensions import db,migrate

# from app.controllers.books_controller import books
# from app.controllers.auth_controller import User
# from app.controllers.companies_controller import company

##load_dotenv()

def create_app():
    
    app = Flask(__name__)  # app instance
    
    app.config.from_object('config.Config')   # Add the configuration class
    
    ##
    db.init_app(app)
    migrate.init_app(app,db)
    # bcrypt.init_app(app)
    # jw.init_app(app)
    
    
    # Importing and registering models
    
    from app.models.users import  User
    from app.models.books import Book
    from app.models.companies import Company
    
    ##
    # Registering blueprints
    # app.register_blueprint(auth)
    # app.register_blueprint(user)
    # app.register_blueprint(company)
    
    @app.route("/")
    def home():
        return "AUTHORS API PROJECT"
    
    return app



if __name__=='__main__':
    app = create_app()
    app.run(debug=True)

