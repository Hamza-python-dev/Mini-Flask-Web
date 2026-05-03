# 🎓 EduPortal — Flask Web Application

A full-stack web application built with **Python & Flask** that handles student admissions, contact forms, financial plan requests, and an admin dashboard — all with email notifications and file uploads.

---

## 🚀 Live Features

| Feature | Description |
|---|---|
| 🏠 Homepage | Welcoming landing page for the institute |
| 📋 Admission Form | Full student registration with file uploads (photo & CNIC) |
| 📬 Contact Form | Message submission with email notification to admin |
| 💰 Financial Plan | Students can request financial assistance |
| 🔐 Admin Dashboard | Secure login to view and delete all submissions |
| 📧 Email Alerts | Auto emails sent to both admin and user on form submission |
| 🗄️ SQLite Database | All data stored persistently using SQLAlchemy ORM |

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite + Flask-SQLAlchemy
- **Email:** Flask-Mail (Gmail SMTP)
- **Frontend:** HTML, CSS, Jinja2 Templates
- **File Handling:** Werkzeug (secure uploads)
- **Environment:** python-dotenv

---

## 📁 Project Structure

```
flask-web-app/
│
├── app.py                  # Main Flask application
├── data.db                 # SQLite database (auto-created)
├── .env                    # Secret keys (NOT uploaded to GitHub)
├── .env.example            # Template for environment variables
├── requirements.txt        # All dependencies
│
├── static/
│   ├── uploads/            # Uploaded photos and CNIC files
│   └── css/                # Stylesheets
│
└── templates/
    ├── index.html          # Homepage
    ├── about-us.html       # About page
    ├── our-services.html   # Services page
    ├── contact.html        # Contact form
    ├── admission.html      # Admission form
    ├── login.html          # Admin login
    ├── dashboard.html      # Admin dashboard
    └── email_template.html # HTML email template
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password_here
MAIL_USE_SSL=True
MAIL_USE_TLS=False

ADMIN_EMAIL=admin@example.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=yourpassword
```

> ⚠️ **Important:** Never upload your `.env` file to GitHub. It's already in `.gitignore`.

> 💡 **Gmail Tip:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833) instead of your real password.

### 5. Initialize the Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('DB created!')"
```

### 6. Run the App

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser 🎉

---

## 🔐 Admin Panel

Navigate to `/login` and use your admin credentials from `.env`.

The dashboard lets you:
- View all contact messages
- View all admission applications
- View all financial plan requests
- Delete any record

---

## 📋 Environment Variables Reference

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session encryption key |
| `MAIL_SERVER` | SMTP server (e.g. smtp.gmail.com) |
| `MAIL_PORT` | SMTP port (465 for SSL) |
| `MAIL_USERNAME` | Your Gmail address |
| `MAIL_PASSWORD` | Gmail App Password |
| `MAIL_USE_SSL` | Set to `True` for port 465 |
| `ADMIN_EMAIL` | Email to receive notifications |
| `ADMIN_USERNAME` | Admin login username |
| `ADMIN_PASSWORD` | Admin login password |

---

## 📦 Requirements

Create this file by running:
```bash
pip freeze > requirements.txt
```

Key packages used:
```
Flask
Flask-Mail
Flask-SQLAlchemy
python-dotenv
Werkzeug
```

---

## 🙅 What's in `.gitignore`

Make sure your `.gitignore` includes:

```
.env
data.db
__pycache__/
*.pyc
venv/
static/uploads/
```

---

## 🔮 Future Improvements

- [ ] Add ML model to predict admission eligibility based on marks
- [ ] Add pagination to the admin dashboard
- [ ] Add email verification for applicants
- [ ] Deploy to Render or Railway (free hosting)
- [ ] Add student login portal

---

## 👨‍💻 Author

**Hamza**
- Learning Python, Flask & Machine Learning
- Building real-world projects step by step 🚀

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
