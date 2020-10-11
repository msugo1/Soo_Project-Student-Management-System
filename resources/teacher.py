from werkzeug.security import  safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

"""
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

_user_parser =
_user_parser =
(_ means private so should not import it somewhere else)


class AdminLogin(Resource):
    parser

    @classmethod
    def post(self):
        # get data from parser
        # find user in database
        # check password
        # create access token
        # create refresh token

        data = cls.parser.parse_args() -> _user_parser.parse_args()
        admin = AdminModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

"""