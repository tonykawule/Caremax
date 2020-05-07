from flask_login import UserMixin
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, index=True)
    password_hash = db.Column(db.String(90), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    #is_admin = db.Column(db.Boolean, default=False)
    #is_doctor = db.Column(db.Boolean, default=False)
    
    def __init__(self, firstname, lastname, username, email, password_hash, role):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

class Patient(db.Model):
    __tablename__='patients'
    id = db.Column(db.Integer, primary_key=True)
    registrationnumber = db.Column(db.String(10), nullable=False, unique=True)
    healthcareunit = db.Column(db.String(50), nullable=False,)
    patientname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    dob = db.Column(db.String(10))
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

    def __init__(self,registrationnumber, healthcareunit, patientname, gender, dob, address, contact, nextofkin, contactphone, religion, tribe, profession, bloodgroup, allergy):
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
    __tablename__='visitations'
    id = db.Column(db.Integer, primary_key=True)
    visitationdate = db.Column(db.String(10), nullable=False)
    presentcomplaint = db.Column(db.String(100), nullable=False)
    previouscomplaint = db.Column(db.String(100), nullable=False)
    labrecommendation = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, visitationdate, presentcomplaint, previouscomplaint, labrecommendation, patient_id):
        self.visitationdate=visitationdate
        self.presentcomplaint=presentcomplaint
        self.previouscomplaint=previouscomplaint
        self.labrecommendation=labrecommendation
        self.patient_id=patient_id


class Appointment(db.Model):
    __tablename__='appointments'
    id = db.Column(db.Integer, primary_key=True)
    appointmentdate = db.Column(db.String(10), nullable=False) 
    appointmenttime = db.Column(db.String(8), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, appointmentdate, appointmenttime, contact, message, patient_id ):
        self.appointmentdate=appointmentdate
        self.appointmenttime=appointmenttime
        self.contact=contact
        self.message=message
        self.patient_id=patient_id

class Payment(db.Model):
    __tablename__='payments'
    id=db.Column(db.Integer, primary_key=True)
    paymentdate=db.Column(db.String(50), nullable=False)
    amountpaid=db.Column(db.Float)
    balance=db.Column(db.Float)
    payeename=db.Column(db.String(50), nullable=False)
    naration=db.Column(db.String(60), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, paymentdate, amountpaid, balance, payeename, naration, patient_id):
        self.paymentdate=paymentdate
        self.amountpaid=amountpaid
        self.balance=balance
        self.payeename=payeename
        self.naration=naration
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
    __tablename__='treatments'
    id=db.Column(db.Integer, primary_key=True) 
    diagnosis=db.Column(db.String(40), nullable=False)
    treatment=db.Column(db.String(150), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, diagnosis, treatment, patient_id):
        self.diagnosis=diagnosis
        self.treatment=treatment
        self.patient_id=patient_id

class Test(db.Model):
    __tablename__='tests'
    id=db.Column(db.Integer, primary_key=True)
    testname=db.Column(db.String(50), nullable=False)
    testresults=db.Column(db.String(150), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, testname, testresults, patient_id):
        self.testname=testname
        self.testresults=testresults
        self.patient_id=patient_id

class Bill(db.Model):
    __tablename__='bills'
    id=db.Column(db.Integer, primary_key=True)
    billdate=db.Column(db.String(10), nullable=False)
    amountbilled=db.Column(db.Float)
    patientname=db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, billdate, amountbilled, patientname, patient_id):
        self.billdate=billdate
        self.amountbilled=amountbilled
        self.patientname=patientname
        self.patient_id=patient_id

db.create_all()


