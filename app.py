from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.login import Userlogin
app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='votersapp'
app.config['PREFERRED_URL_SCHEME']='http'
api=Api(app)
jwt=JWTManager(app)
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401
api.add_resource(Userlogin,'/Userlogin')


if __name__ == "__main__":
    app.run(debug=True)
