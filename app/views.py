from app import app
from flask import render_template, request, redirect, url_for, flash
from .models import User, Patient, Payment, Visitation, Test, Treatment, Bill, Appointment, Healthcareunit
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegistrationForm, LoginForm, PatientForm, PaymentForm, BillForm, TreatmentForm, VisitationForm, TestForm, AppointmentForm,HealthcareunitForm
from app import forms


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
#@login_required
def registration():
    if request.method =='GET':
        user = User.query.all()
        return render_template('registration.html', user=user)
        
    if request.method =='POST':
        form = RegistrationForm()
        if form.validate_on_submit():
            username = request.form['username']
            email = request.form['email']
            password_hash = request.form['password_hash']
            role = request.form['role']
            user = User(username=username,email=email,password_hash=generate_password_hash(password_hash, method='sha256'), role=role)
            db.session.add(user)
            db.session.commit()
            user = User.query.all()
            flash(f'Account has been successfully created for {form.username.data}, you can now Login please', 'success')
            return redirect(url_for('login'))
        else:
            return render_template('newregistration.html', form=form)
    return render_template('login.html', title='Login', form=form)

@app.route("/registration/newregistration") 
#@login_required   
def newregistration():
   form = RegistrationForm()
   return render_template('newregistration.html', form=form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user, current_user, duration=None)
                flash('welcome to caremax please get started', 'info')
                return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful, please try again', 'warning')               
    return render_template('login.html', title='login', form=form)
    
@app.route('/logout') 
def logout():
    logout_user()
    return redirect(url_for('login')) 
     
#PATIENT BLOCK
@app.route("/patient/", methods = ["POST", "GET"])
@login_required
def patient():
    if request.method =='GET':
        patient = Patient.query.all()
        return render_template('patient.html', patient=patient)
    
    if request.method =='POST':
        form = PatientForm(request.form)
        registrationnumber=request.form['registrationnumber']
        healthcareunit=request.form['healthcareunit']
        patientname=request.form['patientname']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        contact=request.form['contact']
        nextofkin=request.form['nextofkin']
        contactphone=request.form['contactphone']
        religion=request.form['religion']
        tribe=request.form['tribe']
        profession=request.form['profession']
        bloodgroup=request.form['bloodgroup']
        allergy=request.form['allergy']
        patient = Patient(registrationnumber=registrationnumber,healthcareunit=healthcareunit,patientname=patientname,gender=gender,dob=dob,address=address,contact=contact,nextofkin=nextofkin,contactphone=contactphone,religion=religion ,tribe=tribe,profession=profession,bloodgroup=bloodgroup,allergy=allergy)
        db.session.add(patient)
        db.session.commit()
        patient = Patient.query.all()
        flash(f'{form.patientname.data} has been saved successfully!', 'success')
        return redirect(url_for('patient'))
    else:
        return render_template('newpatient.html', form=form)    
    return render_template('patient.html', patient=patient)

@app.route("/patient/newpatient")
@login_required
def newpatient():
    form = PatientForm()
    return render_template('newpatient.html', form=form )  

#edit patient
@app.route("/patient/editpatient/<int:patient_id>", methods= ['GET', 'POST'])
@login_required
def editpatient(patient_id):
    patient = Patient.query.get(patient_id)
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
        flash('Patient information updated successfully', 'success')
        return redirect(url_for('patient'))    
    return render_template('editpatient.html', form=form) 

#delete patient
@app.route("/patient/deletepatient/<int:patient_id>")
@login_required
def deletepatient(patientid):
    patient = Patient.query.get(patientid)
    db.session.delete(patient)
    db.session.commit() 
    flash('Patient deleted successfully!!', 'danger')
    return redirect(url_for('patient'))    

 #end Patient

 #start Visits
@app.route("/visitation", methods=['GET', 'POST'])
@login_required
def visitation(patient_id):
    if request.method =='GET':
        visits = Visitation.query.all()
        return render_template('visitation.html', visits=visits)

    if request.method =='POST':
        form = VisitationForm(request.form)
        if form.validate_on_submit():
            visitationdate = request.form['visitationdate']
            presentcomplaint = request.form['presentcomplaint']
            previouscomplaint = request.form['previouscomplaint'] 
            comment = request.form['comment']
            patient_id = request.form['patient_id']
            visits = Visitation(visitationdate=visitationdate,presentcomplaint=presentcomplaint,previouscomplaint=previouscomplaint,comment=comment,patient_id=patient_id)  
            db.session.add(visits)    
            db.session.commit()
            visits = Visitation.query.all()
            flash(f'Visitation has been submitted successfully!', 'success')
            return redirect(url_for('visitation'))
        else:
           return render_template('newvisitation.html', form=form)    
        return render_template('visitation.html', visits=visits, patient=Patient.query.get(patient_id))

@app.route("/visitation/newvisitation")
@login_required
def newvisitation(patient_id):
    form = VisitationForm()
    return render_template('newvisitation.html', form=form, patient=Patient.query.get(patient_id))

#edit visitation
@app.route("/visitation/editvisitation/<int:visitationid>", methods= ['GET', 'POST'])
@login_required
def editvisitation(visitation_id):
    visit = Visitation.query.get(visitation_id)
    form = VisitationForm(obj=visit)
    if form.validate_on_submit():
        visit.visitationdate = form.visitationdate.data
        visit.presentcomplaint = form.presentcomplaint.data
        visit.previouscomplaint = form.previouscomplaint.data
        visit.comment = form.comment.data
        db.session.commit()
        flash('Patient visitation updated successfully', 'success')
        return redirect(url_for('visitation'))    
    return render_template('editvisitation.html', form=form) 

#delete visitation
@app.route("/visitation/deletevisitation/<int:visitation_id>")
@login_required
def deletevisitation(visitation_id):
    visitation = Visitation.query.get(visitation_id)
    db.session.delete(visitation)
    db.session.commit()
    flash('Visitation deleted successfully!!', 'danger')
    return redirect(url_for('visitation'))        
#end visits

#start Appointment

@app.route("/appointment", methods = ["POST", "GET"])
@login_required
def appointment():
    if request.method =='GET':
        appointments = Appointment.query.all()
        return render_template('appointment.html', appointments=appointments)
    
    if request.method =='POST':
        form = AppointmentForm(request.form)
        if form.validate_on_submit():
            appointmentdate = request.form['appointmentdate']
            appointmenttime = request.form['appointmenttime']
            contact = request.form['contact'] 
            message = request.form['message']
            patient_id = request.form['patient_id']
            appointments = Appointment(appointmentdate=appointmentdate,appointmenttime=appointmenttime,contact=contact,message=message,patientid=patient_id)  
            db.session.add(appointments)    
            db.session.commit()
            appointments = Appointment.query.all()
            flash(f'Your appointment has been submitted successfully!', 'success')
            return redirect(url_for('appointment'))
        else:
           return render_template('newappointment.html', form=form)    
        return render_template('appointment.html', appointments=appointments)

@app.route("/appointment/newappointment")
@login_required
def newappointment():
    form = AppointmentForm()
    return render_template('newappointment.html', form=form)

#edit appointment
@app.route("/appointment/editappointment/<int:appointmentid>", methods= ['GET', 'POST'])
@login_required
def editappointment(appointmentid):
    appointment = Appointment.query.get(appointmentid)
    form = AppointmentForm(obj=appointment)
    if form.validate_on_submit():
        appointment.appointmentdate = form.appointmentdate.data
        appointment.appointmenttime = form.appointmenttime.data
        appointment.contact = form.contact.data
        appointment.message = form.message.data
        db.session.commit()
        flash('Patient appointment updated successfully', 'success')
        return redirect(url_for('appointment'))    
    return render_template('editappointment.html', form=form)    

#delete appointment
@app.route("/appointment/deleteappointment/<int:appointmentid>")
@login_required
def deleteappointment(appointmentid):
    appointment = Appointment.query.get(appointmentid)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!!', 'danger')
    return redirect(url_for('appointment'))     

#end Appointment
#start Payment
@app.route("/payment", methods = ["POST", "GET"])
@login_required
def payment():
    if request.method =='GET':
        payments = Payment.query.all()
        return render_template('payment.html', payments=payments)

    if request.method =='POST':
        form = PaymentForm(request.form)
        if form.validate_on_submit():
            paymentdate = request.form['paymentdate']
            amountpaid = request.form['amountpaid']
            balance = request.form['balance'] 
            payeename = request.form['payeename']
            patient_id = request.form['patient_id']
            payments = Payment(paymentdate=paymentdate,amountpaid=amountpaid,balance=balance,payeename=payeename,patient_id=patient_id)  
            db.session.add(payments)    
            db.session.commit()
            visits = Payment.query.all()
            flash(f'Payment has been submitted successfully!', 'success')
            return redirect(url_for('payment'))
        else:
           return render_template('newpayment.html', form=form)    
        return render_template('payment.html', payments=payments) 

@app.route("/payment/newpayment")
@login_required
def newpayment():
    form = PaymentForm()
    return render_template('newpayment.html', form=form)  

#edit payment
@app.route("/payment/editpayment/<int:paymentid>", methods= ['GET', 'POST'])
@login_required
def editpayment(paymentid):
    payment = Payment.query.get(paymentid)
    form = PaymentForm(obj=payment)
    if form.validate_on_submit():
        payment.paymentdate = form.paymentdate.data
        payment.amountpaid = form.amountpaid.data
        payment.balance = form.balance.data
        payment.payeename = form.payeename.data
        db.session.commit()
        flash('Patient payment updated successfully', 'success')
        return redirect(url_for('payment'))    
    return render_template('editpayment.html', form=form)    

#delete payment
@app.route("/payment/deletepayment/<int:paymentid>")
@login_required
def deletepayment(paymentid):
    payment = Payment.query.get(paymentid)
    db.session.delete(payment)
    db.session.commit()
    flash('Payment deleted successfully!!', 'danger')
    return redirect(url_for('payment'))

#end Payment
#start Bill
@app.route("/bill", methods = ["POST", "GET"])
@login_required
def bill():
    if request.method =='GET':
        bills = Bill.query.all()
        return render_template('bill.html', bills=bills)

    if request.method =='POST':
        form = BillForm(request.form)
        if form.validate_on_submit():
            billdate = request.form['billdate']
            amountbilled = request.form['amountbilled']
            patientname = request.form['patientname']
            patient_id = request.form['patientid'] 
            bills = Bill(billdate=billdate,amountbilled=amountbilled,patientname=patientname,patientid=patient_id)  
            db.session.add(bills)    
            db.session.commit()
            bills = Bill.query.all()
            flash(f'Bill has been submitted successfully!', 'success')
            return redirect(url_for('bill'))
        else:
           return render_template('newbill.html', form=form)    
        return render_template('bill.html', bills=bills)

@app.route("/bill/newbill")
@login_required
def newbill():
    form = BillForm()
    return render_template('newbill.html', form=form)  

#edit bill
@app.route("/bill/editbill/<int:billid>", methods= ['GET', 'POST'])
@login_required
def editbill(billid):
    bill = Bill.query.get(billid)
    form = BillForm(obj=bill)
    if form.validate_on_submit():
        bill.billdate = form.billdate.data
        bill.amountbilled = form.amountbilled.data
        bill.patientname = form.patientname.data
        db.session.commit()
        flash('Patient bill updated successfully', 'success')
        return redirect(url_for('bill'))    
    return render_template('editbill.html', form=form) 

#delete bill
@app.route("/bill/deletebill/<int:billid>")
@login_required
def deletebill(billid):
    bill = Bill.query.get(billid)
    db.session.delete(bill)
    db.session.commit()
    flash('Bill deleted successfully!!', 'danger')
    return redirect(url_for('bill'))       
#end Bill

#start Treatment
@app.route("/treatment", methods = ["POST", "GET"])
@login_required
def treatment():
    if request.method =='GET':
        treatments = Treatment.query.all()
        return render_template('treatment.html', treatments=treatments)

    if request.method =='POST':
        form = TreatmentForm(request.form)
        if form.validate_on_submit():
            diagnosis = request.form['diagnosis']
            treatment = request.form['treatment']
            dosage = request.form['dosage'] 
            patient_id = request.form['patient_id']
            treatments = Treatment(diagnosis=diagnosis,treatment=treatment,dosage=dosage,patient_id=patient_id)  
            db.session.add(treatments)    
            db.session.commit()
            treatments = Treatment.query.all()
            flash(f'Treatment has been submitted successfully!', 'success')
            return redirect(url_for('treatment'))
        else:
           return render_template('newtreatment.html', form=form)    
        return render_template('treatment.html', treatments=treatments)

@app.route("/treatment/newtreatment")
@login_required
def newtreatment():
    form = TreatmentForm()
    return render_template('newtreatment.html', form=form) 

#edit treatment module
@app.route("/treatment/edittreatment/<int:treatmentid>", methods= ['GET', 'POST'])
@login_required
def edittreatement(treatmentid):
    treatment = Treatment.query.get(treatmentid)
    form = TreatmentForm(obj=treatment)
    if form.validate_on_submit():
        treatment.diagnosis = form.diagnosis.data
        treatment.treatment = form.treatment.data
        treatment.dosage = form.dosage.data
        db.session.commit()
        flash('Patient treatment updated successfully', 'success')
        return redirect(url_for('treatment'))    
    return render_template('edittreatment.html', form=form) 

#delete treatment
@app.route("/treatment/deletetreatment/<int:treatmentid>")
@login_required
def deletetreatment(treatmentid):
    treatment = Treatment.query.get(treatmentid)
    db.session.delete(treatment)
    db.session.commit()
    flash('Treatment deleted successfully!!', 'danger')
    return redirect(url_for('treatment'))
       
#end treatment

#start Test
@app.route("/test/", methods = ["POST", "GET"])
@login_required
def test():
    if request.method =='GET':
        tests = Test.query.all()
        return render_template('test.html', tests=tests)

    if request.method =='POST':
        form = TestForm(request.form)
        if form.validate_on_submit():
            testname = request.form['testname']
            testresults = request.form['testresults']
            patient_id = request.form['patient_id']
            tests = Test(testname=testname, testresults=testresults,patient_id=patient_id)
            db.session.add(tests)
            db.session.commit()
            #tests = Test.query.filter_by(patient_id).first() 
            flash('Patient test has been saved successfully!', 'success')
            return redirect(url_for('test'))
        else:
           return render_template('newtest.html', title='Add Test', form=form )  
        return render_template('test.html', tests=tests)

@app.route("/test/newtest")
@login_required
def newtest():
    form = TestForm()
    return render_template('newtest.html', form=form) 
#edit test module

@app.route("/test/edittest/<int:testid>", methods= ['GET', 'POST'])
@login_required
def edittest(testid):
    test = Test.query.get(testid)
    form = TestForm(obj=test)
    if form.validate_on_submit():
        test.testname = form.testname.data
        test.testresults = form.testresults.data
        db.session.commit()
        flash('Patient test updated successfully', 'success')
        return redirect(url_for('test'))    
    return render_template('edittest.html', form=form)
#delete test module
@app.route("/test/deletetest/<int:testid>", methods= ['GET', 'POST'])
@login_required
def deletetest(testid):
    test = Test.query.get(testid)
    db.session.delete(test)
    db.session.commit()
    flash('Test deleted successfully!!', 'danger')
    return redirect(url_for('test'))
#end Test                          

#profile
@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

#Healthcareunit
@app.route("/healthcareunit/", methods = ["POST", "GET"])
@login_required
def healthcareunit():
    if request.method =='GET':
        healthcareunits = Healthcareunit.query.all()
        return render_template('healthcareunit.html', healthcareunits=healthcareunits)

    if request.method =='POST':
        form = HealthcareunitForm(request.form)
        if form.validate_on_submit():
            healthcareunit = request.form['healthcareunit']
            address = request.form['address']
            #patient_id = request.form['patient_id']
            healthcareunits = Healthcareunit(healthcareunit=healthcareunit, address=address)
            db.session.add(healthcareunits)
            db.session.commit()
            #tests = Test.query.filter_by(patient_id).first() 
            flash(' Healthe care unit has been registered successfully!', 'success')
            return redirect(url_for('healthcareunit'))
        else:
           return render_template('newhealthcareunit.html', title='Add Health care unit', form=form )  
        return render_template('healthcareunit.html', healthcareunits=healthcareunits)

@app.route("/healthcareunit/newhealthcareunit") 
def newhealthcareunit():
    return render_template('newhealthcareunit.html')


