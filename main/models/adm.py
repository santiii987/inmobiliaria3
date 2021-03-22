from main import db
class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), nullable = False, unique = True)
    password = db.Column(db.String(40), nullable = False)

class MainMail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(40), unique = True)
    mail_password = db.Column(db.String(40))
    autosend = db.Column(db.Boolean)


# db.drop_all()
db.create_all()
