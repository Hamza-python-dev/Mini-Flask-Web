from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from extensions import db, mail
from models import Contact, Admission, FinancialPlan
from utils import allowed_file, ask_huggingface
from flask_mail import Message
import os, time

portal = Blueprint('portal', __name__)

@portal.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not name or not email or not message:
            flash("All fields are required!", "danger")
            return redirect(url_for('portal.contact'))
        try:
            db.session.add(Contact(name=name, email=email, message=message))
            db.session.commit()
            admin_msg = Message(f"New contact from {name}",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[os.getenv("ADMIN_EMAIL")])
            admin_msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(admin_msg)
            user_msg = Message('Submission received',
                sender=current_app.config['MAIL_USERNAME'], recipients=[email])
            user_msg.body = f"Hi {name}, your message was received!"
            mail.send(user_msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            print("ERROR:", e)
            flash("Error sending message.", "danger")
        return redirect(url_for('portal.contact'))
    return render_template('contact.html')

@portal.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        name = request.form.get('name')
        father_name = request.form.get('father_name')
        CNIC = request.form.get('cnic')
        dob_str = request.form.get('dob')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        address = request.form.get('address')
        last_qualification = request.form.get('qualification')
        marks = request.form.get('marks')
        course = request.form.get('course')
        additional_information = request.form.get('additional_information')
        if not name or not father_name or not email or not course:
            flash("All required fields must be filled!", "danger")
            return redirect(url_for('portal.admission'))
        date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        select_time = datetime.now().time()
        photo = request.files.get('photo')
        cnic_file = request.files.get('cnic_file')
        photo_filename = None
        cnic_filename = None
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if photo and photo.filename and allowed_file(photo.filename):
            photo_filename = f"{int(time.time())}_{secure_filename(photo.filename)}"
            photo.save(os.path.join(upload_folder, photo_filename))
        if cnic_file and cnic_file.filename and allowed_file(cnic_file.filename):
            cnic_filename = f"{int(time.time())}_{secure_filename(cnic_file.filename)}"
            cnic_file.save(os.path.join(upload_folder, cnic_filename))
        try:
            db.session.add(Admission(
                name=name, father_name=father_name, CNIC=CNIC,
                date_of_birth=date_of_birth, gender=gender, email=email,
                phone_number=phone_number, address=address,
                last_qualification=last_qualification, marks=marks,
                course=course, select_time=select_time,
                photo=photo_filename, cnic_file=cnic_filename,
                additional_information=additional_information
            ))
            db.session.commit()
            flash("Admission submitted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Email already exists or error occurred!", "danger")
        return redirect(url_for('portal.admission'))
    return render_template('admission.html')

@portal.route('/financial_plan', methods=['GET', 'POST'])
def financial_plan():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        reason = request.form.get('reason')
        if not name or not email or not subject or not reason:
            flash("All fields are required!", "danger")
            return redirect(url_for('portal.financial_plan'))
        try:
            db.session.add(FinancialPlan(name=name, email=email, subject=subject, reason=reason))
            db.session.commit()
            admin_msg = Message(f"Financial Plan from {name}",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[os.getenv("ADMIN_EMAIL")])
            admin_msg.body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nReason: {reason}"
            mail.send(admin_msg)
            flash("Request submitted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Something went wrong.", "danger")
        return redirect(url_for('portal.financial_plan'))
    return render_template('index.html')

@portal.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'reply': 'Please type a message!'})
    reply = ask_huggingface(user_message)
    return jsonify({'reply': reply})

@portal.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')