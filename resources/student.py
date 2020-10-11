from flask_restful import Resource, reqparse
from models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nick_name',
                        type=str or None,
                        required=True,
                        help="nick_names MUST BE identified"
                        )
    parser.add_argument('year',
                        type=int,
                        required=True,
                        help="years MUST BE identified"
                        )
    parser.add_argument('school',
                        type=str,
                        required=True,
                        help="schools MUST BE identified"
                        )

    def get(self, name):
        students = StudentModel.find_all_by_name(name)
        if len(students) > 1:
            return {f"students with name {name}": [student.json() for student in students]}
        elif len(students) == 1:
            return StudentModel.find_one_by_name(name).json()
        else:
            return {'message': 'Student not found'}, 404

    def post(self, name):
        data = Student.parser.parse_args()
        student = StudentModel(name, **data)

        if StudentModel.find_all_by_name(name) and not data['nick_name'] or StudentModel.find_by_nick_name(data['nick_name']):
            return {"message": "(warning!) some students already have the same name or nick name, "
                               "please identify the nick_name for later use"}, 406
        try:
            student.save_to_db()
        except:
            return {"message": "An error occurred inserting the student"}, 500

        return student.json(), 201

    def delete(self, name):
        students = StudentModel.find_all_by_name(name)
        if len(students) >= 2:
            return {"message": "cannot define which of the students should be deleted,"
                               " please move onto the delete with nick name section",
                    "reference for nick name": [student.json() for student in students]}, 406

        student = StudentModel.find_one_by_name(name)
        if student:
            student.delete_from_db()
            return {'message': 'Student deleted'}
        return {'message': 'Student not founded'}, 404

    def put(self, name):
        data = Student.parser.parse_args()
        students = StudentModel.find_all_by_name(name)
        student = StudentModel.find_one_by_name(name)

        if len(students) >= 2:
            return {"message": "more than one student with the same name exist in the database, "
                               "please use 'put with nick_name' method",
                    "reference for nick name": [student.json() for student in students]}, 406
        elif len(students) == 1:
            student.year, student.school = data['year'], data['school']
            if data['nick_name'] and student.nick_name != data['nick_name']:
                student.nick_name = data['nick_name']
        else:
            student = StudentModel(name, **data)

        student.save_to_db()
        return student.json()


class StudentWithNickName(Resource):  # method with nick_name
    parser = reqparse.RequestParser()
    parser.add_argument('year',
                        type=int,
                        required=True,
                        help="years MUST BE identified"
                        )
    parser.add_argument('school',
                        type=str,
                        required=True,
                        help="schools MUST BE identified"
                        )

    def get(self, nick_name):
        student = StudentModel.find_by_nick_name(nick_name)
        if student:
            return student.json()
        else:
            return {'message': 'Student not founded'}, 404

    def delete(self, nick_name):
        student = StudentModel.find_by_nick_name(nick_name)
        if student:
            student.delete_from_db()
            return {'message': 'Student deleted'}
        return {'message': 'Student not founded'}, 404

    def put(self, nick_name):
        data = StudentWithNickName.parser.parse_args()
        student = StudentModel.find_by_nick_name(nick_name)

        if student:
            student.year, student.school = data['year'], data['school']
        else:
            return {'message': 'Student with the nick name not found'}, 404

        student.save_to_db()

        return student.json()


class StudentList(Resource):
    def get(self):
        return {'students': [student.json() for student in StudentModel.find_all()]}