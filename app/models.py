from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(90), nullable=False)
    role = db.Column(db.String (20), nullable=False)
    
    def __init__(self, username, email, password_hash, role):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role


class Patient(db.Model):
    __tablename__='patient'
    id = db.Column(db.Integer, primary_key=True)
    registrationnumber = db.Column(db.String(10), nullable=False, unique=True)
    healthcareunit = db.Column(db.String(50), nullable=False,)
    patientname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    dob = db.Column(db.String, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    nextofkin = db.Column(db.String(50), nullable=False)
    contactphone = db.Column(db.Integer, nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    tribe = db.Column(db.String(50), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    bloodgroup = db.Column(db.String(4), nullable=False)
    allergy = db.Column(db.String(100), nullable=False)
    visitations = db.relationship('Visitation', backref='patient', lazy="dynamic", cascade="all, delete")
    appointments = db.relationship('Appointment', backref='patient', lazy="dynamic", cascade="all, delete")
    payments = db.relationship('Payment', backref='patient', lazy="dynamic", cascade="all, delete")
    treatments = db.relationship('Treatment', backref='patient', lazy="dynamic", cascade="all, delete")
    bills = db.relationship('Bill', backref='patient', lazy="dynamic", cascade="all, delete")
    tests = db.relationship('Test', backref='patient', lazy="dynamic", cascade="all, delete")

    def __init__(self, registrationnumber, healthcareunit, patientname, gender, dob, address, contact, nextofkin, contactphone, religion, tribe, profession, bloodgroup, allergy):
        self.registrationnumber=registrationnumber
        self.healthcareunit=healthcareunit
        self.patientname=patientname
        self.gender=gender 
        self.dob=dob
        self.address=address
        self.contact=contact
        self.nextofkin=nextofkin
        self.contactphone=contactphone
        self.religion=religion
        self.tribe=tribe
        self.profession=profession
        self.bloodgroup=bloodgroup
        self.allergy=allergy

class Visitation(db.Model):
    __tablename__='visitation'
    id = db.Column(db.Integer, primary_key=True)
    visitationdate = db.Column(db.String(10), nullable=False)
    presentcomplaint = db.Column(db.String(100), nullable=False)
    previouscomplaint = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, visitationdate, presentcomplaint, previouscomplaint, comment, patientid):
        self.visitationdate=visitationdate
        self.presentcomplaint=presentcomplaint
        self.previouscomplaint=previouscomplaint
        self.comment=comment
        self.patient_id=patient_id


class Appointment(db.Model):
    __tablename__='appointment'
    id = db.Column(db.Integer, primary_key=True)
    appointmentdate = db.Column(db.String(10), nullable=False) 
    appointmenttime = db.Column(db.String(8), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, appointmentdate, appointmenttime, contact, message, patient_id ):
        self.appointmentdate=appointmentdate
        self.appointmenttime=appointmenttime
        self.contact=contact
        self.message=message
        self.patient_id=patient_id

class Payment(db.Model):
    __tablename__='payment'
    id=db.Column(db.Integer, primary_key=True)
    paymentdate=db.Column(db.String(50), nullable=False)
    amountpaid=db.Column(db.Float, nullable=False)
    balance=db.Column(db.Float, nullable=False)
    payeename=db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, paymentdate, amountpaid, balance, payeename, patient_id):
        self.paymentdate=paymentdate
        self.amountpaid=amountpaid
        self.balance=balance
        self.payeename=payeename
        self.patient_id=patient_id

class Healthcareunit(db.Model):
    __tablename__='healthcareunit'
    id = db.Column(db.Integer, primary_key=True)
    healthcareunit = db.Column(db.String(50), nullable=False) 
    address = db.Column(db.String(50), nullable=False) 

    def __init__(self, healthcareunit, address):
        self.healthcareunit=healthcareunit
        self.address=address


class Treatment(db.Model):
    __tablename__='treatment'
    id=db.Column(db.Integer, primary_key=True) 
    diagnosis=db.Column(db.String(40), nullable=False)
    treatment=db.Column(db.String(40), nullable=False)
    dosage=db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, diagnosis, treatment, dosage, patient_id):
        self.diagnosis=diagnosis
        self.treatment=treatment
        self.dosage=dosage
        self.patient_id=patient_id

class Test(db.Model):
    __tablename__='test'
    id=db.Column(db.Integer, primary_key=True)
    testname=db.Column(db.String(50), nullable=False)
    testresults=db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, testname, testresults, patient_id):
        self.testname=testname
        self.testresults=testresults
        self.patient_id=patient_id

class Bill(db.Model):
    __tablename__='bill'
    id=db.Column(db.Integer, primary_key=True)
    billdate=db.Column(db.String(10), nullable=False)
    amountbilled=db.Column(db.Float, nullable=False)
    patientname=db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, billdate, amountbilled, patientname, patient_id):
        self.billdate=billdate
        self.amountbilled=amountbilled
        self.patientname=patientname
        self.patient_id=patient_id

db.create_all()

