import json
import flask
import flask_sqlalchemy
import database

def create_app() -> flask.Flask:
    """
    creates a flask application using application factory
    """
    app = flask.Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    from database import db
    db.init_app(app)

    @app.route("/")
    def welcome():
        return "hello world"

    @app.route("/deposit", methods=["POST"])
    def deposit_funds():
        print( "JSON:", flask.request.json ) #DEBUG
        print( "DATA:", flask.request.data ) #DEBUG
        data = json.loads( flask.request.data )
        if not all( key in data for key in ("amount", "username") ):
            return 'failure'
            raise("insufficient information provided")
        database.deposit( data["username"], float(data["amount"]) )
        return 'success'

    @app.route("/register", methods=["POST"])
    def create_user():
        print( "JSON:", flask.request.json ) #DEBUG
        print( "DATA:", flask.request.data ) #DEBUG
        data = json.loads( flask.request.data )
        if not all( key in data for key in ("username", "email", "password") ):
            return 'failure'
            raise("insufficient information provided")
        database.create_user( **data )
        return 'success'

    return app


if __name__ == "__main__":
    create_app().run( debug=True )