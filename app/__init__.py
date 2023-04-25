#__init__ file is used to mark a folder as a package. 
#it also defines the start-up logic for Flask server
from flask import Flask

#code below is the boilerplate code to start a Flask application
def create_app(test_config=None):
    app = Flask(__name__)
    
    #registering the BP from routes file* everytime you make a new bp 
    #you have to register
    from .routes import planets_bp
    app.register_blueprint(planets_bp) 
    
    return app 
