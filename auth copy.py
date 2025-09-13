from flask import redirect, url_for, session, jsonify, request
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()

def init_auth(app):
    """Initialize OAuth for Cognito authentication."""
    oauth = OAuth(app)
    oauth.register(
    name='oidc',
    authority=os.getenv('COGNITO_AUTHORITY'),
    client_id=os.getenv('COGNITO_CLIENT_ID'),
    client_secret=os.getenv('COGNITO_APP_CLIENT_SECRET'),
    server_metadata_url=os.getenv('COGNITO_METADATA_URL'),
    client_kwargs={
        'scope': 'email openid phone',
        'redirect_uri': 'http://localhost:5000/authorize',
        'token_endpoint_auth_method': 'client_secret_post',
        'state': secrets.token_urlsafe(16)
    }
)
    return oauth

def auth_required():
    """Decorator to protect routes requiring authentication."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get('user')
            if not user:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def setup_auth_routes(app, oauth):
    """Set up authentication routes."""
    @app.route('/login')
    def login():
        # Generate a new state token
        state = secrets.token_urlsafe(16)
        session['oauth_state'] = state
        
        # Clear any existing session data except the state
        for key in list(session.keys()):
            if key != 'oauth_state':
                session.pop(key)
        
        return oauth.oidc.authorize_redirect(
            'http://localhost:5000/authorize',
            state=state
        )

    @app.route('/authorize')
    def authorize():
        try:
            # Verify state
            if 'oauth_state' not in session:
                print("No state in session")
                return redirect(url_for('login'))
            
            if request.args.get('state') != session['oauth_state']:
                print("State mismatch")
                return redirect(url_for('login'))
            
            token = oauth.oidc.authorize_access_token()
            user = token['userinfo']
            
            # Clear the state after successful authorization
            session.pop('oauth_state', None)
            
            # Set user session
            session['user'] = user
            return redirect(url_for('index', login=True))
        except Exception as e:
            print(f"Authorization error: {str(e)}")
            session.clear()
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

def get_user_email():
    """Get the email of the logged-in user."""
    user = session.get('user', {})
    return user.get('email', 'Unknown')