from app import app, mail
from flask import render_template, request, redirect, url_for, flash, session
from .models import User, Patient, Payment, Visitation, Test, Treatment, Bill,Family, Account, Schedule
from app import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from .forms import (LoginForm, PatientForm, PaymentForm, BillForm, TreatmentForm, VisitationForm,
                    TestForm, UserForm, FamilyForm, AccountForm, ScheduleForm, RequestResetForm, ResetPasswordForm)
from app import forms
from sqlalchemy.exc import IntegrityError
from app.decorator import ensure_correct_user, prevent_login_signup, requires_access_level
from flask_mail import Message


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# USER SIGN UP


@app.route("/registration", methods=["POST", "GET"])
@login_required
@prevent_login_signup
def registration():
    if request.method == 'GET':
        user = User.query.all()
        return render_template('users/registration.html', user=user)

    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                firstname = form.firstname.data
                lastname = form.lastname.data
                username = form.username.data
                email = form.email.data
                password = form.password.data
                access = form.access.data
                user = User(firstname=firstname, lastname=lastname, username=username, email=email,
                            password=generate_password_hash(password, method='sha256'), access=access)
                db.session.add(user)
                db.session.commit()
                user = User.query.all()
                flash(
                    f'Account has been successfully created for {form.username.data}, you can now Login please', 'success')
                return redirect(url_for('registration'))
            except IntegrityError:
                db.session.rollback()
                flash(f'Email address already taken, please find a unique address',
                      'alert alert-danger')
                return render_template("users/newuser.html", form=form)
        else:
            return render_template('users/newuser.html', form=form)
    return render_template('users/newuser.html', form=form)


@app.route("/newuser")
@login_required
@prevent_login_signup
def newuser():
    form = UserForm()
    return render_template("users/newuser.html", form=form)

# delete User


@app.route("/register/<int:id>/deleteuser")
@login_required
def deleteuser(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User deleted successfully!!', 'danger')
    return redirect(url_for('registration'))

# LOGIN BLOCK


@app.route("/login", methods=["GET", "POST"])
@prevent_login_signup
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, current_user)
                flash(f'Welcome to caremax please get started', 'success')
                return redirect(url_for('dashboard'))
        else:
            flash(
                f'Login unsuccessful, please check your login credentials and try again', 'warning')
    return render_template('login.html', title='login', form=form)

# LOGOUT BLOCK


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have logged out successfully!, can login again', 'success')
    return redirect(url_for('login'))

# PATIENT BLOCK


@app.route("/patient", methods=["POST", "GET"])
@login_required
def patient():
    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        patients = Patient.query.order_by(
            Patient.registrationnumber.desc()).paginate(page=page, per_page=14)
        return render_template("patients/patient.html", patients=patients)

    form = PatientForm(request.form)
    if request.method == "POST":
        try:
            new_patient = Patient(
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
            flash(
                f'{form.patientname.data} account has been successfully created!', 'success')
            return redirect(url_for('patient'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Patient Registration Number already exists and please give a patient a unique RegNo', 'warning')
            return render_template("patients/newpatient.html", form=form)
    return render_template("patients/patient.html", patients=patients)

# NEW PATIENNT


@app.route("/patients/newpatient")
@login_required
def newpatient():
    form = PatientForm()
    return render_template('patients/newpatient.html', form=form)

# edit patient


@app.route("/patients/<int:id>/editpatient", methods=['GET', 'POST'])
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
        flash(f'Patient information updated successfully', 'success')
        return redirect(url_for('patient'))
    return render_template('patients/editpatient.html', form=form)

# delete patient


@app.route("/patient/<int:id>/deletepatient")
@login_required
def deletepatient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    flash(f'Patient deleted successfully!!', 'danger')
    return redirect(url_for('patient'))


@app.route("/patients/<int:patient_id>/print_data")
@login_required
def print_data(patient_id):
    return render_template('patients/print.html', patient=Patient.query.get(patient_id))

# end Patient

# START OF VISITATION
 # see all visits for a specific patient and a new visitation


@app.route('/patients/<int:patient_id>/visitations', methods=["GET", "POST"])
@login_required
def patient_visitation(patient_id):
    # find a patient
    if request.method == 'POST':
        form = VisitationForm(request.form)
        if form.validate_on_submit():
            new_visit = Visitation(form.visitationdate.data, form.presentcomplaint.data,
                                   form.previouscomplaint.data, form.labrecommendation.data, patient_id)
            db.session.add(new_visit)
            db.session.commit()
            flash(f'New visitation for has been successfully saved', 'success')
            return redirect(url_for('patient_visitation', patient_id=patient_id))
        else:
            return render_template('visitations/newvisitation.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))
    return render_template("visitations/visitation.html", patient=Patient.query.get(patient_id))

# New Visitation


@app.route('/patient/<int:patient_id>/visitation', methods=["GET", "POST"])
@login_required
def newvisitation(patient_id):
    form = VisitationForm()
    return render_template('visitations/newvisitation.html', form=form, patient=Patient.query.get(patient_id))

# Edit a patient visitation


@app.route('/patient/<int:patient_id>/visitations/<int:id>/editvisitation', methods=["GET", "POST"])
@login_required
def editvisitation(patient_id, id):
    visitation = Visitation.query.get(id)
    form = VisitationForm(obj=visitation)
    if request.method == 'POST':
        visitation.visitationdate = form.visitationdate.data
        visitation.presentcomplaint = form.presentcomplaint.data
        visitation.previouscomplaint = form.previouscomplaint.data
        visitation.labrecommendation = form.labrecommendation.data
        db.session.commit()
        flash(f'Visitation updated successfully!', 'success')
        return redirect(url_for('patient_visitation', patient_id=patient_id))
    return render_template("visitations/editvisitation.html", form=form, patient=Patient.query.get(patient_id))

# START OF TEST
# see all test for a specific patient and a new visitation


@app.route('/patients/<int:patient_id>/tests', methods=["GET", "POST"])
@login_required
def patient_test(patient_id):
    # find a patient
    if request.method == 'POST':
        form = TestForm(request.form)
        if form.validate_on_submit():
            new_test = Test(form.testname.data,
                            form.testresults.data, patient_id)
            db.session.add(new_test)
            db.session.commit()
            flash(f'New Test for has been successfully saved', 'success')
            return redirect(url_for('patient_test', patient_id=patient_id))
        else:
            return render_template('tests/newtest.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))
    return render_template("tests/test.html", patient=Patient.query.get(patient_id))

# New Test


@app.route('/patient/<int:patient_id>/test', methods=["GET", "POST"])
@login_required
def newtest(patient_id):
    form = TestForm()
    return render_template('tests/newtest.html', form=form, patient=Patient.query.get(patient_id))

# Edit a patient Test


@app.route('/patient/<int:patient_id>/test/<int:id>/edittest', methods=["GET", "POST"])
@login_required
def edittest(patient_id, id):
    test = Test.query.get(id)
    form = TestForm(obj=test)
    if request.method == 'POST':
        test.testname = form.testname.data
        test.testresults = form.testresults.data
        db.session.commit()
        flash(f'Test updated successfully!', 'success')
        return redirect(url_for('patient_test', patient_id=patient_id))
    return render_template("tests/edittest.html", form=form, patient=Patient.query.get(patient_id))

# End of Test

# START OF TREATMENT
# see all test for a specific patient and a new treatment


@app.route('/patients/<int:patient_id>/treatments', methods=["GET", "POST"])
@login_required
def patient_treatment(patient_id):
    # find a patient
    if request.method == 'POST':
        form = TreatmentForm(request.form)
        if form.validate_on_submit():
            new_treatment = Treatment(
                form.treatment_date.data, form.diagnosis.data, form.treatment.data, patient_id)
            db.session.add(new_treatment)
            db.session.commit()
            flash(f'New Treatment for has been successfully saved', 'success')
            return redirect(url_for('patient_treatment', patient_id=patient_id))
        else:
            return render_template('treatments/newtreatment.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))
    return render_template("treatments/treatment.html", patient=Patient.query.get(patient_id))

# New Test


@app.route('/patient/<int:patient_id>/treatment', methods=["GET", "POST"])
@login_required
def newtreatment(patient_id):
    form = TreatmentForm()
    return render_template('treatments/newtreatment.html', form=form, patient=Patient.query.get(patient_id))

# Edit a patient Treatment


@app.route('/patient/<int:patient_id>/treatments/<int:id>/edittreatment', methods=["GET", "POST"])
@login_required
def edittreatment(patient_id, id):
    treatment = Treatment.query.get(id)
    form = TreatmentForm(obj=treatment)
    if request.method == 'POST':
        treatment.treatment_date = form.treatment_date.data
        treatment.diagnosis = form.diagnosis.data
        treatment.treatment = form.treatment.data
        db.session.commit()
        flash(f'Treatment updated successfully!', 'success')
        return redirect(url_for('patient_treatment', patient_id=patient_id))
    return render_template("treatments/edittreatment.html", form=form, patient=Patient.query.get(patient_id))

# START OF PAYMENT
 # see all payment for a specific patient and a new payment


@app.route('/patients/<int:patient_id>/payments', methods=["GET", "POST"])
@login_required
def patient_payment(patient_id):

    # find a patient
    if request.method == 'POST':
        form = PaymentForm(request.form)
        if form.validate_on_submit():
            new_payment = Payment(form.paymentdate.data, form.amountpaid.data,
                                  form.balance.data, form.payeename.data, form.narration.data, patient_id)
            db.session.add(new_payment)
            db.session.commit()
            flash(f'New Payment for has been successfully saved', 'success')
            return redirect(url_for('patient_payment', patient_id=patient_id))
        else:
            return render_template('payments/newpayment.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))
    return render_template("payments/payment.html", patient=Patient.query.get(patient_id))

# New Payment


@app.route('/patient/<int:patient_id>/payment', methods=["GET", "POST"])
@login_required
def newpayment(patient_id):
    form = PaymentForm()
    return render_template('payments/newpayment.html', form=form, patient=Patient.query.get(patient_id))

# Edit a patient payment


@app.route('/patient/<int:patient_id>/payments/<int:id>/editpayment', methods=["GET", "POST"])
@login_required
def editpayment(patient_id, id):
    payment = Payment.query.get(id)
    form = PaymentForm(obj=payment)
    if request.method == 'POST':
        payment.paymentdate = form.paymentdate.data
        payment.amountpaid = form.amountpaid.data
        payment.balance = form.balance.data
        payment.payeename = form.payeename.data
        payment.narration = form.narration.data
        db.session.commit()
        flash(f'Payment updated successfully!', 'success')
        return redirect(url_for('patient_payment', patient_id=patient_id))
    return render_template("payments/editpayment.html", form=form, patient=Patient.query.get(patient_id))

# START OF BILL
 # see all bill for a specific patient and a new payment


@app.route('/patients/<int:patient_id>/bills', methods=["GET", "POST"])
@login_required
def patient_bill(patient_id):

    # find a patient
    if request.method == 'POST':
        form = BillForm(request.form)
        if form.validate_on_submit():
            new_bill = Bill(form.billdate.data, form.amountbilled.data,
                            form.patientname.data, patient_id)
            db.session.add(new_bill)
            db.session.commit()
            flash(f'New Bill for has been successfully saved', 'success')
            return redirect(url_for('patient_bill', patient_id=patient_id))
        else:
            return render_template('bills/newbill.html', form=form, patient_id=patient_id, patient=Patient.query.get(patient_id))
    return render_template("bills/bill.html", patient=Patient.query.get(patient_id))

# New Bill


@app.route('/patient/<int:patient_id>/bill', methods=["GET", "POST"])
@login_required
def newbill(patient_id):
    form = BillForm()
    return render_template('bills/newbill.html', form=form, patient=Patient.query.get(patient_id))

# Edit a patient payment


@app.route('/patient/<int:patient_id>/bills/<int:id>/editbill', methods=["GET", "POST"])
@login_required
def editbill(patient_id, id):
    bill = Bill.query.get(id)
    form = BillForm(obj=bill)
    if request.method == 'POST':
        bill.billdate = form.billdate.data
        bill.amountbilled = form.amountbilled.data
        bill.patientname = form.patientname.data
        db.session.commit()
        flash(f'Bill updated successfully!', 'success')
        return redirect(url_for('patient_bill', patient_id=patient_id))
    return render_template("bills/editbill.html", form=form, patient=Patient.query.get(patient_id))


# START OF FAMILY FILES
@app.route("/family", methods=["POST", "GET"])
@login_required
def family():
    if request.method == "GET":
        families = Family.query.all()
        return render_template("family_file/family.html", families=families)

    form = FamilyForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_family = Family(
                    form.family_name.data,
                    form.location.data,
                    form.family_contact.data)
                db.session.add(new_family)
                db.session.commit()
                flash(
                    f'{form.family_name.data} account has been successfully created!', 'success')
                return redirect(url_for('family'))
            except IntegrityError:
                db.session.rollback()
                flash(f'Family name already exists please find another name!', 'warning')
                return render_template("family_file/newfamily.html", form=form)
        else:
            return render_template("family_file/newfamily.html", form=form)
    return render_template("family_file/family.html", families=families)


@app.route("/newfamily")
@login_required
def newfamily():
    form = FamilyForm()
    return render_template("family_file/newfamily.html", form=form)


@app.route("/family/<int:id>/editfamily", methods=['GET', 'POST'])
@login_required
def editfamily(id):
    family = Family.query.get(id)
    form = FamilyForm(obj=family)
    if request.method == 'POST':
        if form.validate_on_submit():
            family.family_name = form.family_name.data
            family.location = form.location.data
            family.family_contact = form.family_contact.data
            db.session.commit()
            flash(f'Family information updated successfully', 'success')
            return redirect(url_for('family'))
        else:
            return render_template("family_file/editfamily.html", form=form)
    return render_template('family_file/editfamily.html', form=form)


@app.route("/family/<int:id>/deletefamily")
@login_required
def deletefamily(id):
    family = Family.query.get(id)
    db.session.delete(family)
    db.session.commit()
    flash(f'Family deleted successfully!!', 'danger')
    return redirect(url_for('family'))

# ACCOUNT MODULE


@app.route('/families/<int:family_id>/accounts', methods=["GET", "POST"])
@login_required
def accounts(family_id):
    # find a patient
    if request.method == 'POST':
        form = AccountForm(request.form)
        if form.validate_on_submit():
            new_account = Account(form.patient_name.data, form.visiteddate.data,
                                  form.treatment.data, form.bill.data, form.bill_narration.data,
                                  form.payment.data,
                                  form.payment_narration.data, family_id)
            db.session.add(new_account)
            db.session.commit()
            flash(
                f'New faily file for {form.patient_name.data} has been successfully saved', 'success')
            return redirect(url_for('accounts', family_id=family_id))
        else:
            return render_template('accounts/newaccount.html', form=form, family_id=family_id, family=Family.query.get(family_id))
    return render_template("accounts/account.html", family=Family.query.get(family_id))

# NEW ACCOUNT


@app.route('/family/<int:family_id>/accounts', methods=["GET", "POST"])
@login_required
def newaccount(family_id):
    form = AccountForm()
    return render_template('accounts/newaccount.html', form=form, family=Family.query.get(family_id))

# EDIT ACCOUNT DETAILS


@app.route('/family/<int:family_id>/accounts/<int:id>/editaccount', methods=["GET", "POST"])
@login_required
def editaccount(family_id, id):
    accounts = Account.query.get(id)
    form = AccountForm(obj=accounts)
    if request.method == 'POST':
       # accounts.patient_name = form.patient_name.data
        accounts.visiteddate = form.visiteddate.data
        accounts.treatment = form.treatment.data
        accounts.bill = form.bill.data
        accounts.bill_narration = form.bill_narration.data
        accounts.payment = form.payment.data
        accounts.payment_narration = form.payment_narration.data
        db.session.commit()
        flash(f'Account updated successfully!', 'success')
        return redirect(url_for('accounts', family_id=family_id))
    return render_template("accounts/editaccount.html", form=form, family=Family.query.get(family_id))


@app.route("/schedule", methods=["POST", "GET"])
@login_required
def schedule():
    if request.method == "GET":
        schedules = Schedule.query.all()
        return render_template("schedule/schedule.html", schedules=schedules)

    form = ScheduleForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_schedule = Schedule(
                    form.schedule_date.data,
                    form.work_schedule.data,
                    form.created_by.data)
                db.session.add(new_schedule)
                db.session.commit()
                flash(f'Schedule has been successfully created!', 'success')
                return redirect(url_for('schedule'))
            except IntegrityError:
                db.session.rollback()
                flash(f'Date already exists please look at your Calender!', 'warning')
                return render_template("schedule/addnew.html", form=form)
        else:
            return render_template("schedule/addnew.html", form=form)
    return render_template("schedule/schedule.html", schedules=schedules)


@app.route("/addnew")
@login_required
def new_schedule():
    form = ScheduleForm()
    return render_template("schedule/addnew.html", form=form)


@app.route("/schedule/<int:id>/editschedule", methods=['GET', 'POST'])
@login_required
def editschedule(id):
    schedule = Schedule.query.get(id)
    form = ScheduleForm(obj=schedule)
    if request.method == 'POST':
        if form.validate_on_submit():
            schedule.schedule_date = form.schedule_date.data
            schedule.work_schedule = form.work_schedule.data
            schedule.created_by = form.created_by.data
            db.session.commit()
            flash(f'Schedule information updated successfully', 'success')
            return redirect(url_for('schedule'))
        else:
            return render_template("schedule/editschedule.html", form=form)
    return render_template('schedule/editschedule.html', form=form)


@app.route("/schedule/<int:id>/deleteschedule")
@login_required
def deleteschedule(id):
    schedule = Schedule.query.get(id)
    db.session.delete(schedule)
    db.session.commit()
    flash(f'Schedule deleted successfully!!', 'danger')
    return redirect(url_for('schedule'))

# ERROR HANDLER FUNCTION


@app.errorhandler(403)
def permission_denied(e):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


'''
@app.errorhandler(500)
def system_down(e):
    return render_template("errors/500.html"), 500
'''

'''
PASSWORD RESET IN CASE PASSWORD HAS BEEN FORGOTTEN
'''


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreply@caremax.com', recipients=[user.email])
    msg.body = f''' To reset your password, please visit the following link:
{url_for('reset_token', token=token, _external=True)}  

No changes will take effect if you ignore this email.

'''
    mail.send(msg)


@app.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent with instructions to reset your Password', 'info')
        return redirect(url_for('login'))
    return render_template("request_reset.html", form=form)


@app.route('/reset_token/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    user = User.verify_reset_token(token)

    if user is None:
        flash(f'That is an expired or invalid token, please make your request over again', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            password = form.password.data

            user = User(password=generate_password_hash(
                password, method='sha256'))
            user.password = password
            db.session.commit()
            flash(
                f'Password has been successfully updated, you can now Login please', 'success')
            return redirect(url_for('login'))

    return render_template("reset_token.html", form=form)

# Restricting Routes
