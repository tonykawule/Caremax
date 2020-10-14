from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, app
from datetime import datetime

ACCESS = {
    'user' : 1,
    'admin' : 2    
}

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(90), nullable=False)
    access = db.Column(db.String(10), nullable=False)

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
           s = Serializer(app.config['SECRET_KEY'])
           try:
               user_id = s.loads(token) ['user_id']
           except:
               return None
           return User.query.get(user_id)

    def __init__(self, firstname, lastname, username, email, password, access=ACCESS['user']):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.access = access 

    def is_admin(self):
        return self.access == ACCESS['admin']  

    def allowed(self, access_level):
        return self.access >= access_level                

class Patient(db.Model):
    __tablename__='patients'
    id = db.Column(db.Integer, primary_key=True)
    registrationnumber = db.Column(db.String(10), nullable=False, unique=True)
    healthcareunit = db.Column(db.String(50), nullable=False,)
    patientname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    dob = db.Column(db.String(10))
    address = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    nextofkin = db.Column(db.String(50), nullable=False)
    contactphone = db.Column(db.String(15), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    tribe = db.Column(db.String(50), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    bloodgroup = db.Column(db.String(4), nullable=False)
    allergy = db.Column(db.String(100), nullable=False)
    visitations = db.relationship('Visitation', backref='patient', lazy="dynamic", cascade="all, delete")
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
        self.patient_id= patient_id

class Payment(db.Model):
    __tablename__='payments'
    id=db.Column(db.Integer, primary_key=True)
    paymentdate=db.Column(db.String(50), nullable=False)
    amountpaid=db.Column(db.Integer, nullable=False)
    balance=db.Column(db.String, nullable=False)
    payeename=db.Column(db.String(50), nullable=False)
    narration=db.Column(db.String(60), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, paymentdate, amountpaid, balance, payeename, narration, patient_id):
        self.paymentdate=paymentdate
        self.amountpaid=amountpaid
        self.balance=balance
        self.payeename=payeename
        self.narration=narration
        self.patient_id=patient_id

class Treatment(db.Model):
    __tablename__='treatments'
    id=db.Column(db.Integer, primary_key=True)
    treatment_date = db.Column(db.String(10), nullable=False) 
    diagnosis=db.Column(db.String(40), nullable=False)
    treatment=db.Column(db.String(150), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self,treatment_date, diagnosis, treatment, patient_id):
        self.treatment_date=treatment_date
        self.diagnosis=diagnosis
        self.treatment=treatment
        self.patient_id=patient_id

class Test(db.Model):
    __tablename__='tests'
    id=db.Column(db.Integer, primary_key=True)
    testname = db.Column(db.String(50), nullable=False)
    testresults = db.Column(db.String(150), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, testname, testresults, patient_id):
        self.testname=testname
        self.testresults=testresults
        self.patient_id=patient_id

class Bill(db.Model):
    __tablename__='bills'
    id=db.Column(db.Integer, primary_key=True)
    billdate=db.Column(db.String(10), nullable=False)
    amountbilled=db.Column(db.Integer)
    patientname=db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, billdate, amountbilled, patientname, patient_id):
        self.billdate=billdate
        self.amountbilled=amountbilled
        self.patientname=patientname
        self.patient_id=patient_id


class Family(db.Model):
    __tablename__='families'
    id = db.Column(db.Integer, primary_key=True)
    family_name = db.Column(db.String(30), unique=True, nullable=False)
    location = db.Column(db.String(50), nullable=False) 
    family_contact = db.Column(db.String(15), nullable=False) 
    accounts = db.relationship('Account', backref='family', lazy="dynamic", cascade="all, delete")   

    def __init__(self, family_name, location, family_contact):
        self.family_name = family_name
        self.location = location
        self.family_contact = family_contact

class Account(db.Model):
    __tablename__='accounts'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(30), nullable=False)
    visiteddate = db.Column(db.String(10), nullable=False)
    treatment = db.Column(db.String(50), nullable=False)
    bill = db.Column(db.String, nullable=False)
    bill_narration = db.Column(db.String(50), nullable=False)
    payment = db.Column(db.String, nullable=False)
    payment_narration = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('families.id'))

    def __init__(self, patient_name, visiteddate, treatment, bill, bill_narration, payment, payment_narration, family_id):
        self.patient_name = patient_name
        self.visiteddate = visiteddate
        self.treatment = treatment
        self.bill = bill
        self.bill_narration = bill
        self.payment = payment
        self.payment_narration = payment_narration
        self.family_id = family_id

class Schedule(db.Model):
    __tablename__='schedules'
    id = db.Column(db.Integer, primary_key=True)
    schedule_date = db.Column(db.String(10), nullable=False)
    work_schedule = db.Column(db.String(1000), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)

    def __init__(self, schedule_date, work_schedule, created_by):
        self.schedule_date = schedule_date
        self.work_schedule = work_schedule
        self.created_by = created_by
    

db.create_all()


