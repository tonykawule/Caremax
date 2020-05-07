from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, Email, ValidationError, InputRequired
from app.models import User

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', [validators.DataRequired(), Length(min=5, max=20, message='First name must be between 5 to 20 characters')])
    lastname = StringField('Last Name', [validators.DataRequired(), Length(min=5, max=20, message='Last name must be between 5 to 20 characters')])
    username = StringField('Username', [validators.DataRequired(), Length(min=5, max=20, message='Username must be between 5 to 20 characters')])
    email = StringField('Email', [validators.DataRequired(),Email(), Length(min=8, max=30, message='Email must be between 8 to 30 characters')])
    password_hash = PasswordField('Password', [validators.DataRequired(), Length(min=6, max=20, message='Password must be between 8 to 30 characters')])
    role = StringField('Role', [validators.DataRequired(), Length(min=5, max=20, message='Role must be between 5 to 20 characters')])


class LoginForm(FlaskForm):
     username = StringField('Username', [validators.DataRequired(), Length(min=5, max=20, message='Username must be between 5 to 20 characters')])
     password_hash = PasswordField('Password', [validators.DataRequired(), Length(min=6, max=20, message='Password must be between 6 to 20 characters')])
     

class PatientForm(FlaskForm):
    registrationnumber = StringField('Registrationnumber', [validators.DataRequired(), Length(min=3, max=10, message='RegNo must be between 3 to 10 characters')])
    healthcareunit = StringField('Health care unit', [validators.DataRequired(), Length(min=8, max=30, message='Unit name must be between 8 to 30 characters')])
    patientname = StringField('Patient name', [validators.DataRequired(), Length(min=8, max=30, message='Patient name must be between 8 to 30 characters')])
    gender = StringField('Gender', [validators.DataRequired(), Length(min=8, max=30, message='Gender must be  4 and 6 characters')])
    dob = StringField('Date of Birth', [validators.DataRequired(), Length(min=10, max=10, message='Date must be  10 characters')]) 
    address = StringField('Address', [validators.DataRequired(), Length(min=8, max=30, message='Address must be between 5 to 30 characters')])
    contact = StringField('Contact', [validators.DataRequired(), Length(min=10, max=13, message='Contact must be between 10 to 13 characters')])
    nextofkin = StringField('Next of kin', [validators.DataRequired(), Length(min=8, max=30, message='Name must be between 8 to 30 characters')]) 
    contactphone = StringField('Contact phone', [validators.DataRequired(), Length(min=10, max=13, message='Contact must be between 8 to 30 characters')]) 
    religion = StringField('Religion', [validators.DataRequired(), Length(min=5, max=12, message='Religion must be between 8 to 30 characters')]) 
    tribe = StringField('Tribe', [validators.DataRequired(), Length(min=5, max=20, message='Tribe must be between 5 to 20 characters')])
    profession = StringField('Profession', [validators.DataRequired(), Length(min=5, max=20, message='Profession must be between 5 to 20 characters')]) 
    bloodgroup = StringField('Bloodgroup', [validators.DataRequired(), Length(min=2, max=3, message='Bloodgroup must be between 2 to 3 characters')]) 
    allergy = TextAreaField('Allergy', [validators.DataRequired(), Length(min=4, max=50, message='Allergy must be between 4 to 50 characters')])
        
class VisitationForm(FlaskForm):
    visitationdate = StringField('Visitation date', [validators.DataRequired(), Length(min=10, max=10, message='Date must be  10 characters')])
    presentcomplaint = TextAreaField('Present Complaint', [validators.DataRequired(), Length(min=4, max=30, message='Present complaint must be between 4 to 30 characters')])
    previouscomplaint = TextAreaField('Previous Complaint', [validators.DataRequired(), Length(min=4, max=30, message='Previous complaint must be between 4 to 30 characters')])
    labrecommendation = TextAreaField('Comment', [validators.DataRequired(), Length(min=8, max=30, message='Comment must be between 8 to 30 characters')])
       

class AppointmentForm(FlaskForm):
    appointmentdate = StringField('Appointment date', [validators.DataRequired(), Length(min=10, max=10, message='Date must be  10 characters')])
    appointmenttime = StringField('Appointment time', [validators.DataRequired(), Length(min=3, max=6, message='Time must be  3 to 6 characters')])
    contact = StringField('Contact', [validators.DataRequired(), Length(min=10, max=13, message='Contact must be  10 to 13 characters')])
    message = TextAreaField('Message', [validators.DataRequired(), Length(min=10, max=50, message='Message must be between 10 and 50 characters')])
    

class PaymentForm(FlaskForm):
    paymentdate = StringField('Payment date', [validators.DataRequired(), Length(min=10, max=10, message='Date must be  10 characters')])
    amountpaid = IntegerField('Amount Paid')
    balance = IntegerField('Balance')
    payeename = StringField('Payee Name', [validators.DataRequired(), Length(min=8, max=30, message='Payee name must be between 8 and 30 characters')])
    naration = TextAreaField('Naration', [validators.DataRequired(), Length(min=8, max=60, message='Payee name must be between 8 and 60 characters')])
     

class BillForm(FlaskForm):
    billdate = StringField('Bill date', [validators.DataRequired(), Length(min=10, max=10, message='Date must be  10 characters')])
    amountbilled = IntegerField('Amount Bill')
    patientname = StringField('Patient Name', [validators.DataRequired(), Length(min=8, max=30, message='Payee name must be between 8 to 30 characters')])
    

class TreatmentForm(FlaskForm):
    diagnosis = StringField('Diagnosis', [validators.DataRequired(), Length(min=5, max=20, message='Diagnosis must be between 5 to 20 characters')])
    treatment = StringField('Treatment Name', [validators.DataRequired(), Length(min=5, max=150, message='Treatment must be between 5 to 30 characters')])
    

class TestForm(FlaskForm):
    testname = StringField('Test Name', [validators.DataRequired(), Length(min=3, max=40, message='Test name must be between 3 to 40 characters')])
    testresults = TextAreaField('Test Results', [validators.DataRequired(), Length(min=8, max=150, message='Test results  must be between 8 to 100 characters')])

class HealthcareunitForm(FlaskForm):
    healthcareunit = StringField('Health care unit', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])

                    