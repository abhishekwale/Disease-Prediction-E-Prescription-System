Disease Prediction System
Deployed App: 
               https://disease-prediction-e-prescription-system.onrender.com
A Flask-based web application that predicts diseases based on symptoms using machine learning. The system includes user authentication via AWS Cognito and email notifications via AWS SES.
Prerequisites

Python 3.10 or higher
Docker (optional, for containerized deployment)
AWS Account with Cognito and SES services configured
Git (optional, for version control)
AWS CLI and EB CLI (optional, for Elastic Beanstalk deployment)

Setup Instructions
1. Clone and Setup Environment
# Clone the repository
git clone https://github.com/abhishekwale/Disease-Prediction-E-Prescription-System
cd Disease-Prediction-E-Prescription-System

# Create and activate virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

2. AWS Configuration
AWS Cognito Setup

Go to AWS Console → Amazon Cognito
Create a new User Pool
Note down:
User Pool ID
App Client ID
App Client Secret


Configure the app client:
Add http://localhost:5000/authorize (local) or https://disease.onrender.com/authorize (Render) as a callback URL
Add http://localhost:5000/login (local) or https://disease.onrender.com/login (Render) as a sign-out URL
Enable required OAuth flows (e.g., Authorization Code Grant)



AWS SES Setup

Go to AWS Console → Amazon SES
Verify your email address or domain
Note down the verified sender email address

3. Environment Configuration
Create a .env file in the project root with:
# AWS Cognito Configuration
COGNITO_CLIENT_ID=your_client_id_here
COGNITO_APP_CLIENT_SECRET=your_client_secret_here
COGNITO_AUTHORITY=https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_QVTpc40WC
COGNITO_METADATA_URL=https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_QVTpc40WC/.well-known/openid-configuration
COGNITO_REDIRECT_URI=http://localhost:5000/authorize
COGNITO_SIGNOUT_URI=http://localhost:5000/login

# AWS Region
AWS_REGION=ap-south-1

# AWS SES Configuration
SES_SENDER_EMAIL=your-verified-email@domain.com

# Flask Secret Key
SECRET_KEY=your-secret-key-here

For Render deployment, update:
COGNITO_REDIRECT_URI=https://disease.onrender.com/authorize
COGNITO_SIGNOUT_URI=https://disease.onrender.com/login

4. Run the Application Locally
# Ensure virtual environment is activated
python main.py

Visit http://localhost:5000 to test the Cognito login flow.
5. Dockerize the Application (Optional)

Build Docker image:docker build -t healthcare .


Run locally:docker run --env-file .env -p 5000:5000 healthcare



6. Deploy to Render

Push Docker image to Docker Hub:docker tag healthcare yourusername/healthcare:latest
docker push yourusername/healthcare:latest


In Render Dashboard:
Create a Web Service with Docker environment.
Set image to docker.io/yourusername/healthcare:latest.
Add environment variables from .env (use Render’s Environment tab).
Set Port to 5000.
Deploy and visit https://disease.onrender.com.



7. Deploy to AWS Elastic Beanstalk (Alternative)

Install EB CLI: pip install awsebcli
Initialize: eb init -p docker myFlaskApp --region ap-south-1
Create environment: eb create my-flask-env --single
Set environment variables:eb setenv COGNITO_CLIENT_ID=your_client_id COGNITO_APP_CLIENT_SECRET=your_client_secret COGNITO_AUTHORITY=https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_QVTpc40WC COGNITO_METADATA_URL=https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_QVTpc40WC/.well-known/openid-configuration COGNITO_REDIRECT_URI=https://my-flask-env.ap-south-1.elasticbeanstalk.com/authorize COGNITO_SIGNOUT_URI=https://my-flask-env.ap-south-1.elasticbeanstalk.com/login AWS_REGION=ap-south-1 SES_SENDER_EMAIL=your-verified-email@domain.com SECRET_KEY=your-secret-key-here


Deploy: eb deploy

Features

Disease prediction based on symptoms
User authentication via AWS Cognito
Email notifications with prediction results
Nearby doctor search functionality
Prediction history logging
Secure session management

Project Structure
Disease-Prediction-E-Prescription-System/
├── main.py              # Main application file
├── auth.py             # Authentication configuration
├── prediction.py       # Disease prediction logic
├── email_system.py     # Email notification system
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (not in git)
├── .dockerignore      # Docker ignore file
├── Dockerfile         # Docker configuration
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── kaggle_dataset/    # Dataset files
└── model/            # ML model files

Security Notes

Never commit the .env file to version control
Keep your AWS credentials secure
Regularly update dependencies for security patches
For large kaggle_dataset/ or model/ files, use AWS S3 and update prediction.py to download them

Troubleshooting

Authentication Issues

Verify Cognito configuration in AWS Console
Ensure callback/sign-out URLs match exactly in Cognito and .env
Check environment variables


Email Sending Issues

Verify SES email address/domain
Check AWS region configuration
Ensure proper IAM permissions


Prediction Issues

Verify dataset and model files exist
Ensure all dependencies are installed


Docker/Render Issues

Use linux/amd64 platform: docker buildx build --platform linux/amd64 -t yourusername/healthcare:latest --push .
Check Render logs for errors



Contributing

Fork the repository
Create a feature branch (git checkout -b dev)
Commit changes (git commit -m "Add feature")
Push to the branch (git push origin dev)
Create a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.