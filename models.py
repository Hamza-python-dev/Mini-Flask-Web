from extensions import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    CNIC = db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(100))
    last_qualification = db.Column(db.String(50))
    marks = db.Column(db.Integer)
    course = db.Column(db.String(100))
    select_time = db.Column(db.Time)
    photo = db.Column(db.String(200))
    cnic_file = db.Column(db.String(200))
    additional_information = db.Column(db.Text)

class FinancialPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    subject = db.Column(db.String(200))
    reason = db.Column(db.String(100))