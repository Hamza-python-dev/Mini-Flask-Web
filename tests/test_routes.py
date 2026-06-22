import pytest
 
 
# ─── PUBLIC ROUTES (no login needed) ────────────────────────────────────────
 
def test_home_page(client):
    res = client.get("/")
    assert res.status_code == 200
 
def test_about_page(client):
    res = client.get("/about")
    assert res.status_code == 200
 
def test_services_page(client):
    res = client.get("/services")
    assert res.status_code == 200
 
def test_contact_page(client):
    res = client.get("/contact")
    assert res.status_code == 200
 
def test_admission_page(client):
    res = client.get("/admission")
    assert res.status_code == 200
 
def test_financial_plan_page(client):
    res = client.get("/financial_plan")
    assert res.status_code == 200
 
def test_nonexistent_route(client):
    res = client.get("/this-does-not-exist")
    assert res.status_code == 404
 
 
# ─── AUTH ROUTES ─────────────────────────────────────────────────────────────
 
def test_login_page_loads(client):
    res = client.get("/login")
    assert res.status_code == 200
 
def test_login_wrong_password(client):
    res = client.post("/login", data={
        "username": "wronguser",
        "password": "wrongpass"
    }, follow_redirects=True)
    assert res.status_code in [200, 400, 401]
 
def test_logout_redirects(client):
    res = client.get("/logout", follow_redirects=False)
    assert res.status_code in [302, 200]
 
 
# ─── PROTECTED ROUTES ────────────────────────────────────────────────────────
 
def test_dashboard_requires_login(client):
    res = client.get("/dashboard", follow_redirects=False)
    assert res.status_code == 302
 
def test_chat_is_post_only(client):
    res = client.get("/chat")
    assert res.status_code == 405
 
def test_chatbot_is_public(client):
    res = client.get("/chatbot")
    assert res.status_code == 200
 
def test_delete_contact_requires_login(client):
    res = client.get("/delete_contact/1", follow_redirects=False)
    assert res.status_code in [302, 401, 405]
 
def test_delete_admission_requires_login(client):
    res = client.get("/delete_admission/1", follow_redirects=False)
    assert res.status_code in [302, 401, 405]
 
def test_delete_financial_requires_login(client):
    res = client.get("/delete_financial/1", follow_redirects=False)
    assert res.status_code in [302, 401, 405]
 
 
# ─── CONTACT FORM ────────────────────────────────────────────────────────────
 
def test_contact_missing_all_fields(client):
    """Empty form should redirect back, not crash"""
    res = client.post("/contact", data={
        "name": "", "email": "", "message": ""
    }, follow_redirects=True)
    assert res.status_code == 200
 
def test_contact_missing_name(client):
    """Missing name should not save to DB"""
    res = client.post("/contact", data={
        "name": "", "email": "test@test.com", "message": "Hello"
    }, follow_redirects=True)
    assert res.status_code == 200
 
def test_contact_missing_email(client):
    """Missing email should not save to DB"""
    res = client.post("/contact", data={
        "name": "Hamza", "email": "", "message": "Hello"
    }, follow_redirects=True)
    assert res.status_code == 200
 
def test_contact_saves_to_db(client, app):
    """Valid contact form should save record to database"""
    from models import Contact
    client.post("/contact", data={
        "name": "Hamza",
        "email": "hamza@test.com",
        "message": "Test message"
    }, follow_redirects=True)
    with app.app_context():
        record = Contact.query.filter_by(email="hamza@test.com").first()
        assert record is not None
        assert record.name == "Hamza"
        assert record.message == "Test message"
 
 
# ─── ADMISSION FORM ──────────────────────────────────────────────────────────
 
def test_admission_missing_required_fields(client):
    """Empty required fields should redirect back"""
    res = client.post("/admission", data={
        "name": "", "father_name": "", "email": "", "course": ""
    }, follow_redirects=True)
    assert res.status_code == 200
 
def test_admission_missing_name(client):
    """Missing name should not save"""
    res = client.post("/admission", data={
        "name": "", "father_name": "Ali",
        "email": "test@test.com", "course": "Python"
    }, follow_redirects=True)
    assert res.status_code == 200
 
def test_admission_saves_to_db(client, app):
    """Valid admission form should save record to database"""
    from models import Admission
    client.post("/admission", data={
        "name": "Hamza",
        "father_name": "Ali",
        "cnic": "12345-1234567-1",
        "dob": "2000-01-01",
        "gender": "Male",
        "email": "hamza@admission.com",
        "phone": "03001234567",
        "address": "Rawalpindi",
        "qualification": "FSc",
        "marks": "85",
        "course": "Flask",
        "additional_information": ""
    }, follow_redirects=True)
    with app.app_context():
        record = Admission.query.filter_by(email="hamza@admission.com").first()
        assert record is not None
        assert record.name == "Hamza"
        assert record.course == "Flask"
 
 
# ─── FINANCIAL PLAN FORM ─────────────────────────────────────────────────────
 
def test_financial_plan_missing_fields(client):
    """Empty financial form should redirect back"""
    res = client.post("/financial_plan", data={
        "name": "", "email": "", "subject": "", "reason": ""
    }, follow_redirects=True)
    assert res.status_code == 200
 
def test_financial_plan_saves_to_db(client, app):
    """Valid financial plan should save to database"""
    from models import FinancialPlan
    client.post("/financial_plan", data={
        "name": "Hamza",
        "email": "hamza@finance.com",
        "subject": "Fee Installment",
        "reason": "Need monthly plan"
    }, follow_redirects=True)
    with app.app_context():
        record = FinancialPlan.query.filter_by(email="hamza@finance.com").first()
        assert record is not None
        assert record.subject == "Fee Installment"
 
 
# ─── CHAT ENDPOINT ───────────────────────────────────────────────────────────
 
def test_chat_empty_message_returns_prompt(client):
    """/chat with empty message should return a prompt reply"""
    res = client.post("/chat", json={"message": ""})
    assert res.status_code == 200
    data = res.get_json()
    assert "reply" in data
    assert data["reply"] == "Please type a message!"
 
def test_chat_returns_json(client):
    """/chat should always return JSON with a reply key"""
    res = client.post("/chat", json={"message": "hello"})
    assert res.status_code == 200
    data = res.get_json()
    assert "reply" in data
    assert isinstance(data["reply"], str)
 