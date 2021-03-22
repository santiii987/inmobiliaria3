from main import db

class Subscribers(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(40), nullable = False, unique = True)

class Contactquestions(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer)
    complete_name = db.Column(db.String(40), nullable = False)
    phone = db.Column(db.Integer)
    mail = db.Column(db.String(40), nullable = False)
    question = db.Column(db.String(200), nullable = False)
    answered = db.Column(db.Boolean, default = False)
    read = db.Column(db.Boolean, default = False)
    saved = db.Column(db.Boolean, default = False)
    erased = db.Column(db.Boolean, default = False)

# db.drop_all()
# db.create_all()
