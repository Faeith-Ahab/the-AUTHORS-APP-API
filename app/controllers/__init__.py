import extensions

from app import create_app

                                     #defined blueprints
from app.controllers.auth_controller import auth
from app.controllers.companies_controller import company
from app.controllers.books_controller import books

#load_dotenv()


#application factory function
 
