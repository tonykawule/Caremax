from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max=20)])
    password_hash = PasswordField('Password_hash', validators=[DataRequired(), Length(min=4, max=20)])
    role = StringField('Role', validators=[DataRequired(), Length(min=5, max=50)])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists, please use another one')

    def validate_username(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists, please use another one')    


class LoginForm(FlaskForm):
     username = StringField('Username', validators=[DataRequired(), Length(min=5, max=50)])
     password_hash = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
     

class PatientForm(FlaskForm):
    registrationnumber = StringField('Registrationnumber', validators=[DataRequired(), Length(min=5, max=10)])
    healthcareunit = StringField('Health care unit', validators=[DataRequired(), Length(min=8, max=50)])
    patientname = StringField('Patient name', validators=[DataRequired(), Length(min=8, max=20)])
    gender = StringField('Gender', validators=[DataRequired()])
    dob = StringField('Date of Birth', validators=[DataRequired(), Length(min=9, max=10)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=50)])
    contact = StringField('Contact', validators=[DataRequired(), Length(min=5, max=20)])
    nextofkin = StringField('Next of kin', validators=[DataRequired(), Length(min=8, max=50)])
    contactphone = StringField('Contact phone', validators=[DataRequired(), Length(min=5, max=20)])
    religion = StringField('Religion', validators=[DataRequired, Length(min=5, max=20)])
    tribe = StringField('Tribe', validators=[DataRequired(), Length(min=5, max=20)])
    bloodgroup = StringField('Bloodgroup', validators=[DataRequired(), Length(min=2, max=15)])
    allergy = TextAreaField('Allergy', validators=[DataRequired(), Length(min=4, max=100)])
    profession = StringField('Profession', validators=[DataRequired(), Length(min=5, max=50)])
    
class VisitationForm(FlaskForm):
    visitationdate = StringField('Visitation date', validators=[DataRequired(), Length(min=9, max=10)])
    presentcomplaint = TextAreaField('Present Complaint', validators=[DataRequired(), Length(min=5, max=100)])
    previouscomplaint = TextAreaField('Previous Complaint', validators=[DataRequired(), Length(min=5, max=100)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=5, max=100)])
       

class AppointmentForm(FlaskForm):
    appointmentdate = StringField('Appointment date', validators=[DataRequired(), Length(min=9, max=10)])
    appointmenttime = StringField('Appointment time', validators=[DataRequired(), Length(min=3, max=7)])
    contact = StringField('Contact', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=100)])
    

class PaymentForm(FlaskForm):
    paymentdate = StringField('Payment date', validators=[DataRequired(), Length(min=9, max=10)])
    amountpaid = IntegerField('Amount Paid', validators=[DataRequired()])
    balance = IntegerField('Balance', validators=[DataRequired()])
    payeename = StringField('Payee Name', validators=[DataRequired(), Length(min=8, max=50)])
     

class BillForm(FlaskForm):
    billdate = StringField('Bill date', validators=[DataRequired(), Length(min=9, max=10)])
    amountbilled = IntegerField('Amount Bill', validators=[DataRequired()])
    patientname = StringField('Patient Name', validators=[DataRequired(), Length(min=8, max=50)])
    

class TreatmentForm(FlaskForm):
    diagnosis = StringField('Diagnosis', validators=[DataRequired(), Length(min=5, max=40)])
    treatment = StringField('Treatment Name', validators=[DataRequired(), Length(min=5, max=40)])
    dosage = TextAreaField('Dosage', validators=[DataRequired(), Length(min=5, max=100)])
    

class TestForm(FlaskForm):
    testname = StringField('Test Name', validators=[DataRequired(), Length(min=3, max=50)])
    testresults = TextAreaField('Test Results', validators=[DataRequired(), Length(min=8, max=100)])

class HealthcareunitForm(FlaskForm):
    healthcareunit = StringField('Health care unit', validators=[DataRequired(), Length(min=8, max=50)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=8, max=100)])    

                    