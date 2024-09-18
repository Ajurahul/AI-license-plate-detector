import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from jinja2 import Template
from xhtml2pdf import pisa
from LicenseOCR import LicenseOCR, get_image
from User import get_user_credentials, username_exists, add_user
from UserDatabase import UserDatabase
import os
from io import BytesIO
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Configure cache
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)


# Initialize the cache for the OCR model
@cache.cached(timeout=3600, key_prefix='ocr_model')
def load_model():
    processor = LicenseOCR()
    user_db = UserDatabase('license_plate_db.sqlite')
    user_db.add_license_details()
    return processor


# Load the OCR model once
ocr_processor = load_model()

# Database connection
db = UserDatabase('license_plate_db.sqlite')


# Render HTML template
def render_html_template(details):
    with open("templates/template.html") as file:
        print("Started loading temp")
        template = Template(file.read())
        print("Started debug temp")
        return template.render(
            license_no=details[2],
            owner_name=details[3],
            vehicle_details=details[4],
            registration_date=details[5],
            owner_photo=details[8],
            address=details[6],
            phoneno=details[7]
        )


def verify_login(username, entered_password):
    user_credentials = get_user_credentials(username)
    if user_credentials:
        stored_password = user_credentials['password']
        if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password):
            return True, user_credentials['name']
        else:
            return False, None
    else:
        return False, None


def generate_pdf(html_content):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf)
    pdf.seek(0)
    return pdf


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_valid, user_name = verify_login(username.lower(),
                                           password)  # Convert to lowercase for case-insensitive login

        if is_valid:
            session['username'] = user_name
            # flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif username_exists(username):
            flash('Username already exists!', 'danger')
        else:
            add_user(username, name, password)
            flash('User registered successfully! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    result = None
    no_result = False

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            src_img = get_image(uploaded_file)
            ocr_text = ocr_processor.ocr_image(src_img)
            result = db.get_user_details(ocr_text)

            if not result:
                no_result = True

    return render_template('dashboard.html', result=result, no_result=no_result)


@app.route('/download_pdf/<license_no>')
def download_pdf(license_no):
    result = db.get_user_details(license_no)
    print(result)
    if result:
        html_content = render_html_template(result)
        pdf = generate_pdf(html_content)
        return send_file(pdf, as_attachment=True, download_name=f"license_details_{result[2]}.pdf")
    else:
        flash('No information found for this License Plate.', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
