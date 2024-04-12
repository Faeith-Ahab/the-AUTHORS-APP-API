# Creating different instances for different 3rd party libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_migrate import Migrate
##from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


#var     #constructor
db = SQLAlchemy()      #instance
migrate= Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()














