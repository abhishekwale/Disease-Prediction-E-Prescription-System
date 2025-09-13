# Disease Prediction System

A Flask-based web application that predicts diseases based on symptoms using machine learning. The system includes user authentication via AWS Cognito and email notifications via AWS SES.

## Prerequisites

- Python 3.10 or higher
- AWS Account with Cognito and SES services configured
- Git (optional, for version control)

## Setup Instructions

### 1. Clone and Setup Environment
```bash
# Clone the repository (if using git)
git clone https://github.com/abhishekwale/Disease-Prediction-E-Prescription-System
cd myFlaskApp

# Create and activate virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. AWS Configuration

#### AWS Cognito Setup
1. Go to AWS Console → Amazon Cognito
2. Create a new User Pool
3. Note down the following details:
   - User Pool ID
   - App Client ID
   - App Client Secret
4. Configure the app client:
   - Add `http://localhost:5000/authorize` as a callback URL
   - Enable the required OAuth flows

#### AWS SES Setup
1. Go to AWS Console → Amazon SES
2. Verify your email address or domain
3. Note down the verified sender email address

### 3. Environment Configuration

Create a `.env` file in the project root with the following variables:
```env
# AWS Cognito Configuration
COGNITO_APP_CLIENT_ID=your_client_id_here
COGNITO_APP_CLIENT_SECRET=your_client_secret_here
COGNITO_AUTHORITY=https://cognito-idp.us-east-1.amazonaws.com/your-user-pool-id
COGNITO_METADATA_URL=https://cognito-idp.us-east-1.amazonaws.com/your-user-pool-id/.well-known/openid-configuration
COGNITO_REDIRECT_URI=http://localhost:5000/authorize
COGNITO_SIGNOUT_URI=http://localhost:5000/login

# AWS Region
AWS_REGION=us-east-1

# AWS SES Configuration
SES_SENDER_EMAIL=your-verified-email@domain.com

# Flask Secret Key
SECRET_KEY=your-secret-key-here
```

### 4. Run the Application

```bash
# Make sure you're in the project directory and virtual environment is activated
python main.py
```

The application will be available at `http://localhost:5000`

## Features

- Disease prediction based on symptoms
- User authentication via AWS Cognito
- Email notifications with prediction results
- Nearby doctor search functionality
- Prediction history logging
- Secure session management

## Project Structure

```
myFlaskApp/
├── main.py              # Main application file
├── auth.py             # Authentication configuration
├── prediction.py       # Disease prediction logic
├── email_system.py     # Email notification system
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (not in git)
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── kaggle_dataset/    # Dataset files
└── model/            # ML model files
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your AWS credentials secure
- Regularly update dependencies for security patches

## Troubleshooting

1. **Authentication Issues**
   - Verify Cognito configuration in AWS Console
   - Check callback URLs match exactly
   - Ensure environment variables are set correctly

2. **Email Sending Issues**
   - Verify SES email address/domain
   - Check AWS region configuration
   - Ensure proper IAM permissions

3. **Prediction Issues**
   - Verify dataset files are present
   - Check model file exists
   - Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
