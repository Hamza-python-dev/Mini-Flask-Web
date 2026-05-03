from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps
import os
import time
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Load environment variables
load_dotenv()

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

class Admission(db.Model):
    id = db.Column(db.Integer,primary_key=True)
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
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(100))
    email   = db.Column(db.String(120))
    subject = db.Column(db.String(200))
    reason  = db.Column(db.String(100))

# Secret key
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise ValueError("SECRET_KEY is not set in .env")
# Helper function for boolean values
def str_to_bool(value):
    return str(value).lower() in ["true", "1", "yes"]

# Mail configuration
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 465))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_SSL'] = str_to_bool(os.getenv("MAIL_USE_SSL", True))
app.config['MAIL_USE_TLS'] = str_to_bool(os.getenv("MAIL_USE_TLS", False))


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
mail = Mail(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template("index.html", name="HAMZA", title='Home page')

@app.route('/about')
def about():
    return render_template("about-us.html", title="About us page")

@app.route('/services')
def services():
    return render_template('our-services.html', title='services we offer')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        # Get form data safely
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validation
        if not name or not email or not message:
            flash("All fields are required!", "danger")
            return redirect(url_for('contact'))

        

        try:
            new_message =  Contact(
            name = name,
            email = email,
            message = message
        )
            db.session.add(new_message)
            db.session.commit()
            admin_msg = Message(
                subject=f"New contact message from {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[os.getenv("ADMIN_EMAIL")]
            )

            admin_msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            admin_msg.html = render_template(
                "email_template.html",
                name=name,
                email=email,
                message=message
            )
            mail.send(admin_msg)

            user_cong=Message(
                subject='Submission form',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            user_cong.body=f"Hi {name},\n\nEmail has been sent succesfully"
            mail.send(user_cong)

            

            flash("Message sent successfully!", "success")

        except Exception as e:
            print("MAIL ERROR:", e)
            flash("Error sending message. Try again later.", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html')


# Config
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Make sure folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)




@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        # Get form data
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

        # Validate required fields
        if not name or not father_name or not email or not course:
            flash("All required fields must be filled!", "danger")
            return redirect(url_for('admission'))

        # Convert string inputs to correct types
        date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        select_time = datetime.now().time()

        # Handle file uploads
        photo = request.files.get('photo')
        cnic_file = request.files.get('cnic_file')
        
        photo_filename = None
        cnic_filename = None

        if photo and photo.filename and allowed_file(photo.filename):
            photo_filename = f"{int(time.time())}_{secure_filename(photo.filename)}"
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        else:
            flash("Invalid photo file type!", "danger")

        if cnic_file and cnic_file.filename and allowed_file(cnic_file.filename):
            cnic_filename = f"{int(time.time())}_{secure_filename(cnic_file.filename)}"
            cnic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], cnic_filename))
        else:
            flash("Invalid CNIC file type!", "danger")
        # Create new Admission record
        new_admission = Admission(
            name=name,
            father_name=father_name,
            CNIC=CNIC,
            date_of_birth=date_of_birth,
            gender=gender,
            email=email,
            phone_number=phone_number,
            address=address,
            last_qualification=last_qualification,
            marks=marks,
            course=course,
            select_time=select_time,
            photo=photo_filename,
            cnic_file=cnic_filename,
            additional_information=additional_information
        )

        try:
            db.session.add(new_admission)
            db.session.commit()
            flash("Admission submitted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            print("DB ERROR:", e)
            flash("Email already exists or error occurred!", "danger")
            return redirect(url_for('admission'))
        
        return redirect(url_for('admission'))

    return render_template('admission.html')

@app.route('/financial_plan', methods=['GET', 'POST'])
def financial_plan():
    if request.method == 'POST':
        name    = request.form.get('name')
        email   = request.form.get('email')
        subject = request.form.get('subject')
        reason  = request.form.get('reason')

        if not name or not email or not subject or not reason:
            flash("All fields are required!", "danger")
            return redirect(url_for('financial_plan'))

        try:
            entry = FinancialPlan(
                name=name,
                email=email,
                subject=subject,
                reason=reason
            )
            db.session.add(entry)
            db.session.commit()

            # Notify admin
            admin_msg = Message(
                subject=f"New Financial Plan Request from {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[os.getenv("ADMIN_EMAIL")]
            )
            admin_msg.body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nReason: {reason}"
            mail.send(admin_msg)

            # Confirm to user
            user_msg = Message(
                subject="We received your Financial Plan request",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            user_msg.body = f"Hi {name},\n\nThank you! We have received your request and will be in touch shortly."
            mail.send(user_msg)

            flash("Request submitted successfully!", "success")

        except Exception as e:
            db.session.rollback()  # ← this was the key missing piece
            print("ERROR:", e)
            flash("Something went wrong. Please try again.", "danger")

        return redirect(url_for('financial_plan'))

    return render_template('index.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Wrong username or password!")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    contacts = Contact.query.all()
    admissions = Admission.query.all()
    financials = FinancialPlan.query.all()
    return render_template('dashboard.html', 
                           contacts=contacts, 
                           admissions=admissions, 
                           financials=financials)

@app.route('/delete_contact/<int:id>')
@login_required
def delete_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_admission/<int:id>')
@login_required
def delete_admission(id):
    admission = Admission.query.get(id)
    db.session.delete(admission)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_financial/<int:id>')
@login_required
def delete_financial(id):
    financial = FinancialPlan.query.get(id)
    db.session.delete(financial)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
