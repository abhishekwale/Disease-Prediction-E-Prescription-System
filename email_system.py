import boto3
import json
import os

# AWS SES Client with default region
ses_client = boto3.client('ses', region_name=os.getenv('AWS_REGION', 'us-east-1'))  # Default to us-east-1 if not set

def send_prediction_email(user_email, prediction_data, pincode):
    predicted_disease = prediction_data['predicted_disease']
    symptoms = prediction_data['symptoms']
    precautions = prediction_data['precautions']
    medications = prediction_data['medications']
    diet = prediction_data['diet']
    
    # Google Maps URL for nearby doctors
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
    }.get(predicted_disease, f"hospital for {predicted_disease}")
    maps_url = f"https://www.google.com/maps/search/{specialty.replace(' ', '+')}+near+{pincode}"

    try:
        response = ses_client.send_email(
            Source=os.getenv('SES_SENDER_EMAIL'),  # Use sender email from .env
            Destination={'ToAddresses': [user_email]},
            Message={
                'Subject': {'Data': 'Your Disease Prediction Results'},
                'Body': {
                    'Text': {
                        'Data': f'''
Dear User,

Your recent disease prediction result: {predicted_disease}

Symptoms Provided:
{", ".join(symptoms)}

Precautions:
{json.dumps(precautions, indent=2)}

Recommended Medications (Consult a Doctor):
{json.dumps(medications, indent=2)}

Recommended Diet:
{json.dumps(diet, indent=2)}

Find Nearby Doctors:
{maps_url}

Note: This information is for informational purposes only. Please consult a healthcare professional for accurate diagnosis and treatment.

Best,
Health App Team
'''
                    }
                }
            }
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False