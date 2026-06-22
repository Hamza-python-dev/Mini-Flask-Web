from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from models import Contact, Admission, FinancialPlan
from blueprints.auth import login_required

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
        contacts=Contact.query.all(),
        admissions=Admission.query.all(),
        financials=FinancialPlan.query.all())

@admin.route('/delete_contact/<int:id>')
@login_required
def delete_contact(id):
    db.session.delete(db.session.get(Contact, id))
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_admission/<int:id>')
@login_required
def delete_admission(id):
    db.session.delete(db.session.get(Admission, id))
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_financial/<int:id>')
@login_required
def delete_financial(id):
    db.session.delete(db.session.get(FinancialPlan, id))
    db.session.commit()
    return redirect(url_for('admin.dashboard'))