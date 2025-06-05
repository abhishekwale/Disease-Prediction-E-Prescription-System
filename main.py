from flask import Flask, request, render_template, redirect, url_for, session
from auth import init_auth, setup_auth_routes, get_user_email, auth_required
from prediction import process_symptoms, get_prediction_logs
from email_system import send_prediction_email
from dotenv import load_dotenv
import os
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Configure session with a secure secret key
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600,  # 1 hour
    SESSION_REFRESH_EACH_REQUEST=True
)

# Initialize OAuth for Cognito
oauth = init_auth(app)
setup_auth_routes(app, oauth)

@app.route('/')
def index():
    user_email = get_user_email()
    login_success = request.args.get('login', False)  # Check for login parameter
    return render_template('index.html', user_email=user_email, login_success=bool(login_success))

@app.route('/home')
@auth_required()
def home():
    user_email = get_user_email()
    return render_template('home.html', user_email=user_email)

@app.route('/predict', methods=['GET', 'POST'])
#@auth_required()
def predict():
    user_email = get_user_email()
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        # Handle comma-separated symptoms from text input
        text_symptoms = request.form.get('symptoms', '').split(',')
        symptoms.extend([s.strip() for s in text_symptoms if s.strip()])
        pincode = request.form.get('pincode', '')
        
        prediction_data, error = process_symptoms(symptoms, user_email, pincode)
        
        if error:
            return render_template('index.html', message=error, user_email=user_email)
        
        session['predicted_disease'] = prediction_data['predicted_disease']
        session['pincode'] = pincode  # Store pincode for logs
        # Send email if pincode is provided
        email_sent = False
        if pincode:
            email_sent = send_prediction_email(user_email, {**prediction_data, 'symptoms': symptoms}, pincode)
        
        return render_template('index.html', 
                             symptoms=symptoms,
                             predicted_disease=prediction_data['predicted_disease'],
                             dis_des=prediction_data['dis_des'],
                             my_precautions=prediction_data['precautions'],
                             medications=prediction_data['medications'],
                             my_diet=prediction_data['diet'],
                             workout=prediction_data['workout'],
                             email_sent=email_sent,
                             user_email=user_email)
    
    return render_template('index.html', user_email=user_email)

@app.route('/search-maps', methods=['POST'])
@auth_required()
def search_maps():
    pincode = request.form['pincode']
    disease = session.get('predicted_disease', '')
    specialty = {
        "Heart attack": "cardiology hospital",
        "Headache": "neurologist clinic",
        "Fungal infection": "dermatologist clinic",
        "Diabetes": "endocrinologist hospital",
        "Asthma": "pulmonologist clinic",
        "Covid-19": "covid care center",
        "Dengue": "general hospital",
        "Acidity": "gastroenterologist clinic",
        "Migraine": "neurologist hospital",
        "Back pain": "orthopedic clinic"
    }.get(disease, f"hospital for {disease}")
    maps_url = f"https://www.google.com/maps/search/{specialty.replace(' ', '+')}+near+{pincode}"
    return redirect(maps_url)

@app.route('/logs')
@auth_required()
def logs():
    user_email = get_user_email()
    user_logs = get_prediction_logs(user_email)
    for log in user_logs:
        log['pincode'] = log.get('pincode', session.get('pincode', 'Not provided'))
    return render_template('logs.html', logs=user_logs, user_email=user_email)

if __name__ == '__main__':
    app.run(debug=True)