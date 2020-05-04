from app import app
from flask import render_template, request, redirect, url_for, flash
from .models import User, Patient, Payment, Visitation, Test, Treatment, Bill, Appointment, Healthcareunit
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegistrationForm, LoginForm, PatientForm, PaymentForm, BillForm, TreatmentForm, VisitationForm, TestForm, AppointmentForm,HealthcareunitForm
from app import forms
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/doctor")
def doctors():
    return render_template('doctors.html')

@app.route("/departments")
def departments():
    return render_template('departments.html') 

@app.route("/about")
def about():
    return render_template('about.html')        

@app.route("/elements")
def elements():
    return render_template('elements.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/single-blog")
def singleblog():
    return render_template('single-blog.html')

@app.route("/blog")
def blog():
    return render_template('blog.html') 

@app.route("/contact")
def contact():
    return render_template('contact.html')               

@app.route("/registration", methods = ["POST", "GET"])
@login_required
def registration():
    if request.method =='GET':
        user = User.query.all()
        return render_template('register/registration.html', user=user)
        
    if request.method =='POST':
        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            try:
                username = form.username.data
                email = form.email.data
                password_hash = form.password_hash.data
                role = form.role.data
                user = User(username=username,email=email,password_hash=generate_password_hash(password_hash, method='sha256'), role=role)
                db.session.add(user)
                db.session.commit()
                user = User.query.all()
                flash(f'Account has been successfully created for {form.username.data}, you can now Login please', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash(f'Username already taken, please find another username', 'alert alert-danger')
                return render_template("register/newregistration.html", form=form)
        else:
            return render_template('register/newregistration.html', form=form)
    return render_template('login.html', title='Login', form=form)

@app.route("/register/newregistration") 
@login_required   
def newregistration():
   form = RegistrationForm()
   return render_template('register/newregistration.html', form=form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user, current_user)
                flash('Welcome to caremax please get started', 'success')
                return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful, please check your login credentials and try again', 'warning')               
    return render_template('login.html', title='login', form=form)
    
@app.route('/logout') 
def logout():
    logout_user()
    flash(f'You have logged out successfully!, can login again', 'success')
    return redirect(url_for('login')) 
     
#PATIENT BLOCK
@app.route("/patient", methods = ["POST", "GET"])
@login_required
def patient():
    if request.method =="GET":
        patients=Patient.query.all()
        return render_template("patients/patient.html", patients=patients)
    form = PatientForm(request.form)
    if request.method =="POST":
        try:
            new_patient= Patient(
                form.registrationnumber.data, 
                form.healthcareunit.data, 
                form.patientname.data,
                form.gender.data,
                form.dob.data,
                form.address.data,
                form.contact.data,
                form.nextofkin.data,
                form.contactphone.data,
                form.religion.data,
                form.tribe.data,
                form.profession.data,
                form.bloodgroup.data,
                form.allergy.data)  
            db.session.add(new_patient)
            db.session.commit()
            flash(f'{form.patientname.data} account has been successfully created!', 'success')
            return redirect(url_for('patient'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Patient Registration Number already exists and please give a patient a unique RegNo', 'warning') 
            return render_template("patients/newpatient.html", form=form) 
    return render_template("patients/patient.html", patients=patients) 
              
#NEW PATIENNT
@app.route("/patients/newpatient")
@login_required
def newpatient():
    form = PatientForm()
    return render_template('patients/newpatient.html', form=form )  

#edit patient
@app.route("/patients/<int:id>/editpatient", methods= ['GET', 'POST'])
@login_required
def editpatient(id):
    patient = Patient.query.get(id)
    form = PatientForm(obj=patient)
    if request.method == 'POST':
        patient.registrationnumber = form.registrationnumber.data
        patient.healthcareunit = form.healthcareunit.data
        patient.patientname = form.patientname.data
        patient.gender = form.gender.data
        patient.dob = form.dob.data
        patient.address = form.address.data
        patient.contact = form.contact.data
        patient.nextofkin = form.nextofkin.data
        patient.contactphone = form.contactphone.data
        patient.religion = form.religion.data
        patient.tribe = form.tribe.data
        patient.bloodgroup = form.bloodgroup.data
        patient.allergy = form.allergy.data
        patient.profession = form.profession.data
        db.session.commit()
        flash('Patient information updated successfully', 'info')
        return redirect(url_for('patient'))    
    return render_template('patients/editpatient.html', form=form) 

#delete patient
@app.route("/patient/<int:id>/deletepatient")
@login_required
def deletepatient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit() 
    flash('Patient deleted successfully!!', 'danger')
    return redirect(url_for('patient'))    

#end Patient

#START OF VISITATION
 # see all visits for a specific patient and a new visitation
@app.route('/patients/<int:patient_id>/visitations', methods=["GET", "POST"])
@login_required
def patient_visitation(patient_id):
    #find a patient
    if request.method =='POST':
        form = VisitationForm(request.form)
        if form.validate_on_submit():
            new_visit = Visitation(form.visitationdate.data, form.presentcomplaint.data, form.previouscomplaint.data, form.comment.data, patient_id)
            db.session.add(new_visit)
            db.session.commit()
            flash(f'New visitation for has been successfully saved', 'success')
            return redirect(url_for('patient_visitation', patient_id=patient_id))
        else:
           return render_template('visitations/newvisitation.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))                         
    return render_template("visitations/visitation.html", patient=Patient.query.get(patient_id))

#New Visitation
@app.route('/patient/<int:patient_id>/visitation', methods=["GET", "POST"])
@login_required
def newvisitation(patient_id):
    form=VisitationForm()
    return render_template('visitations/newvisitation.html', form=form, patient=Patient.query.get(patient_id))

#Edit a patient visitation
@app.route('/patient/<int:patient_id>/visitations/<int:id>/editvisitation', methods=["GET", "POST"])
@login_required
def editvisitation(patient_id, id):
    visitation = Visitation.query.get(id)
    form = VisitationForm(obj=visitation)
    if request.method == 'POST':
        visitation.visitationdate =  form.visitationdate.data
        visitation.presentcomplaint = form.presentcomplaint.data
        visitation.previouscomplaint = form.previouscomplaint.data
        visitation.comment = form.comment.data
        db.session.commit()
        flash(f'Visitation updated successfully!', 'success')
        return redirect(url_for('patient_visitation', patient_id=patient_id))
    return render_template("visitations/editvisitation.html", form=form, patient=Patient.query.get(patient_id))

#Delete and edit a visit for a specific patient
  
#START OF TEST
 # see all test for a specific patient and a new visitation
@app.route('/patients/<int:patient_id>/tests', methods=["GET", "POST"])
@login_required
def patient_test(patient_id):
    #find a patient
    if request.method =='POST':
        form = TestForm(request.form)
        if form.validate_on_submit():
            new_test = Test(form.testname.data, form.testresults.data, patient_id)
            db.session.add(new_test)
            db.session.commit()
            flash(f'New Test for has been successfully saved', 'success')
            return redirect(url_for('patient_test', patient_id=patient_id))
        else:
           return render_template('tests/newtest.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))                         
    return render_template("tests/test.html", patient=Patient.query.get(patient_id))

#New Test
@app.route('/patient/<int:patient_id>/test', methods=["GET", "POST"])
@login_required
def newtest(patient_id):
    form=TestForm()
    return render_template('tests/newtest.html', form=form, patient=Patient.query.get(patient_id))

#Edit a patient Test
@app.route('/patient/<int:patient_id>/visitation/<int:id>/editvisitation', methods=["GET", "POST"])
def edittest(patient_id, id):
    test = Test.query.get(id)
    form = TestForm(obj=test)
    if request.method == 'POST':
        test.testname =  form.testname.data
        test.testresults = form.testresults.data
        db.session.commit()
        flash(f'Test updated successfully!', 'success')
        return redirect(url_for('patient_test', patient_id=patient_id))
    return render_template("tests/edittest.html", form=form, patient=Patient.query.get(patient_id))

#Delete a visit for a specific patient
#@app.route('/patient/<int:patient_id>/visitation/<int:id>/deletevisitation', methods=["GET", "POST"])
#def patient_visitation(patient_id, id):
#    pass

# End of Test

#START OF TREATMENT
 # see all test for a specific patient and a new visitation
@app.route('/patients/<int:patient_id>/treatments', methods=["GET", "POST"])
@login_required
def patient_treatment(patient_id):
    
    #find a patient
    if request.method =='POST':
        form = TreatmentForm(request.form)
        if form.validate_on_submit():
            new_treatment = Treatment(form.diagnosis.data, form.treatment.data, form.dosage.data, patient_id)
            db.session.add(new_treatment)
            db.session.commit()
            flash(f'New Treatment for has been successfully saved', 'success')
            return redirect(url_for('patient_treatment', patient_id=patient_id))
        else:
           return render_template('treatments/newtreatment.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))                         
    return render_template("treatments/treatment.html", patient=Patient.query.get(patient_id))

#New Test
@app.route('/patient/<int:patient_id>/treatment', methods=["GET", "POST"])
@login_required
def newtreatment(patient_id):
    form=TreatmentForm()
    return render_template('treatments/newtreatment.html', form=form, patient=Patient.query.get(patient_id))

#Edit a patient Treatment
@app.route('/patient/<int:patient_id>/treatments/<int:id>/edittreatment', methods=["GET", "POST"])
@login_required
def edittreatment(patient_id, id):
    treatment = Treatment.query.get(id)
    form = TreatmentForm(obj=treatment)
    if request.method == 'POST':
        treatment.diagnosis =  form.diagnosis.data
        treatment.treatment = form.treatment.data
        treatment.dosage = form.dosage.data
        db.session.commit()
        flash(f'Treatment updated successfully!', 'success')
        return redirect(url_for('patient_treatment', patient_id=patient_id))
    return render_template("treatments/edittreatment.html", form=form, patient=Patient.query.get(patient_id))


#Delete a treatment for a specific patient
#@app.route('/patient/<int:patient_id>/visitation/<int:id>/deletevisitation', methods=["GET", "POST"])
#def patient_visitation(patient_id, id):
#    pass

# End of Treatment

#START OF PAYMENT
 # see all payment for a specific patient and a new payment
@app.route('/patients/<int:patient_id>/payments', methods=["GET", "POST"])
@login_required
def patient_payment(patient_id):
    
    #find a patient
    if request.method =='POST':
        form = PaymentForm(request.form)
        if form.validate_on_submit():
            new_payment = Payment(form.paymentdate.data, form.amountpaid.data, form.balance.data, form.payeename.data, patient_id)
            db.session.add(new_payment)
            db.session.commit()
            flash(f'New Payment for has been successfully saved', 'success')
            return redirect(url_for('patient_payment', patient_id=patient_id))
        else:
           return render_template('payments/newpayment.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))                        
    return render_template("payments/payment.html", patient=Patient.query.get(patient_id))

#New Payment
@app.route('/patient/<int:patient_id>/payment', methods=["GET", "POST"])
@login_required
def newpayment(patient_id):
    form=PaymentForm()
    return render_template('payments/newpayment.html', form=form, patient=Patient.query.get(patient_id))

#Edit a patient payment
@app.route('/patient/<int:patient_id>/payments/<int:id>/editpayment', methods=["GET", "POST"])
@login_required
def editpayment(patient_id, id):
    payment = Payment.query.get(id)
    form = PaymentForm(obj=payment)
    if request.method == 'POST':
        payment.paymentdate =  form.paymentdate.data
        payment.amountpaid = form.amountpaid.data
        payment.balance = form.balance.data
        payment.payeename = form.payeename.data
        db.session.commit()
        flash(f'Payment updated successfully!', 'success')
        return redirect(url_for('patient_payment', patient_id=patient_id))
    return render_template("payments/editpayment.html", form=form, patient=Patient.query.get(patient_id))

#START OF BILL
 # see all bill for a specific patient and a new payment
@app.route('/patients/<int:patient_id>/bills', methods=["GET", "POST"])
@login_required
def patient_bill(patient_id):
    
    #find a patient
    if request.method =='POST':
        form = BillForm(request.form)
        if form.validate_on_submit():
            new_bill = Bill(form.billdate.data, form.amountbilled.data, form.patientname.data, patient_id)
            db.session.add(new_bill)
            db.session.commit()
            flash(f'New Bill for has been successfully saved', 'success')
            return redirect(url_for('patient_bill', patient_id=patient_id))
        else:
           return render_template('bills/newbill.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))                         
    return render_template("bills/bill.html", patient=Patient.query.get(patient_id))

#New Bill
@app.route('/patient/<int:patient_id>/bill', methods=["GET", "POST"])
@login_required
def newbill(patient_id):
    form=BillForm()
    return render_template('bills/newbill.html', form=form, patient=Patient.query.get(patient_id))

#Edit a patient payment
@app.route('/patient/<int:patient_id>/bills/<int:id>/editbill', methods=["GET", "POST"])
@login_required
def editbill(patient_id, id):
    bill = Bill.query.get(id)
    form = BillForm(obj=bill)
    if request.method == 'POST':
        bill.billdate =  form.billdate.data
        bill.amountbilled = form.amountbilled.data
        bill.patientname = form.patientname.data
        db.session.commit()
        flash(f'Bill updated successfully!', 'success')
        return redirect(url_for('patient_bill', patient_id=patient_id))
    return render_template("bills/editbill.html", form=form, patient=Patient.query.get(patient_id))

#Delete a treatment for a specific patient
#@app.route('/patient/<int:patient_id>/visitation/<int:id>/deletevisitation', methods=["GET", "POST"])
#def patient_visitation(patient_id, id):
#    pass

# End of Treatment

#START OF APPOINTMENTS
 # see all bill for a specific patient and a new payment
@app.route('/patients/<int:patient_id>/appointments', methods=["GET", "POST"])
@login_required
def patient_appointment(patient_id):
    
    #find a patient
    if request.method =='POST':
        form = AppointmentForm()
        if form.validate_on_submit():
            new_appointment = Appointment(form.appointmentdate.data, form.appointmenttime.data, form.contact.data, form.message.data, patient_id)
            db.session.add(new_appointment)
            db.session.commit()
            flash(f'Your appointment has been forwarded successfully', 'success')
            return redirect(url_for('patient_appointment', patient_id=patient_id))
        else:
           return render_template('appointments/newappointment.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))                        
    return render_template("appointments/appointment.html", patient=Patient.query.get(patient_id))

#New Appointment
@app.route('/patient/<int:patient_id>/appointment', methods=["GET", "POST"])
@login_required
def newappointment(patient_id):
    form=AppointmentForm()
    return render_template('appointments/newappointment.html', form=form, patient=Patient.query.get(patient_id))

#Edit a patient payment
#@app.route('/patient/<int:patient_id>/visitation/<int:id>/editvisitation', methods=["GET", "POST"])
#def patient_visitation(patient_id, id):
#    pass

#Delete a treatment for a specific patient
#@app.route('/patient/<int:patient_id>/visitation/<int:id>/deletevisitation', methods=["GET", "POST"])
#def patient_visitation(patient_id, id):
#    pass

# End of Treatment