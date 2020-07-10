from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Userlogin(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('user_name',type=str,required=True,help="User name cannot be left blank!")
    parser.add_argument('password',type=str,required=True,help="Password cannot be left blank!")

    def post(self):
        data=self.parser.parse_args()
        user=User.getUserById(data['user_name'])
        try:

            if user and safe_str_cmp(user.password,data['password']):
                access_token=create_access_token(identity=user.user_name,expires_delta=False)
                return  {'access_token':access_token},200
        except:
            return {"message":"Invalid Credentials!"}, 401
        return query(f"""select * from users where user_name={data['user_name']};""")
class User():
    def __init__(self,user_name,password):
        self.user_name=user_name
        self.password=password
    @classmethod
    def getUserById(cls,user_name):
        result=query(f"""select user_name,password from users where user_name='{user_name}'""",return_json=False)
        if len(result)>0:
            return User(result[0]['user_name'],result[0]['password'])
        else:
            return None
