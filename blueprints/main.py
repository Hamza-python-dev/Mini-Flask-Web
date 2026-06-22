from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("index.html", name="HAMZA", title='Home page')

@main.route('/about')
def about():
    return render_template("about-us.html", title="About us page")

@main.route('/services')
def services():
    return render_template('our-services.html', title='services we offer')