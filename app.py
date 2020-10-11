import os

from flask import Flask
from flask_restful import Api

from db import db
from resources.student import Student, StudentWithNickName, StudentList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'soo'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentWithNickName, '/student/nickname/<string:nick_name>')
api.add_resource(StudentList, '/students')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
