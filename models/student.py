from db import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    year = db.Column(db.Integer)
    school = db.Column(db.String(80))
    nick_name = db.Column(db.String(80))

    # classroom_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # classroom = db.relationship('ClassroomModel')

    def __init__(self, name, year, school, nick_name=None):
        if nick_name:
            self.nick_name = nick_name
        self.name = name
        self.year = year
        self.school = school

    def json(self):
        return {
            'name': self.name,
            'id': self.id,
            'nick_name': self.nick_name,
            'year': self.year,
            'school': self.school
        }

    @classmethod
    def find_all_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_one_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # given that nicknames are unique
    @classmethod
    def find_by_nick_name(cls, nick_name):
        return cls.query.filter_by(nick_name=nick_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
