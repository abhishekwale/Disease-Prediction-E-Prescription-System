from flask import redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
from dotenv import load_dotenv
import secrets
from urllib.parse import quote

# Load environment variables
load_dotenv()

def init_auth(app):
    """Initialize OAuth for Cognito authentication."""
    oauth = OAuth(app)
    
    redirect_uri = os.getenv('COGNITO_REDIRECT_URI', 'http://localhost:5000/authorize')
    
    oauth.register(
        name='oidc',
        authority=os.getenv('COGNITO_AUTHORITY'),
        client_id=os.getenv('COGNITO_CLIENT_ID'),
        client_secret=os.getenv('COGNITO_APP_CLIENT_SECRET'),
        server_metadata_url=os.getenv('COGNITO_METADATA_URL'),
        client_kwargs={
            'scope': 'email openid phone',
            'redirect_uri': redirect_uri,
            'token_endpoint_auth_method': 'client_secret_post',
        }
    )
    return oauth


def auth_required():
    """Decorator to protect routes requiring authentication."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                # Instead of redirect to login, we redirect to goodbye page
                # (which has the Login button)
                return redirect(url_for('goodbye'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def setup_auth_routes(app, oauth):
    """Set up authentication routes."""

    @app.route('/login')
    def login():
        # Generate fresh state
        state = secrets.token_urlsafe(16)
        session['oauth_state'] = state
        
        # Clear everything else
        for key in list(session.keys()):
            if key != 'oauth_state':
                session.pop(key)
        
        redirect_uri = os.getenv('COGNITO_REDIRECT_URI', 'http://localhost:5000/authorize')
        
        return oauth.oidc.authorize_redirect(
            redirect_uri,
            state=state
        )


    @app.route('/authorize')
    def authorize():
        try:
            if 'oauth_state' not in session:
                return redirect(url_for('goodbye'))
            
            if request.args.get('state') != session.get('oauth_state'):
                return redirect(url_for('goodbye'))
            
            token = oauth.oidc.authorize_access_token()
            userinfo = token.get('userinfo', {})
            
            session.pop('oauth_state', None)
            session['user'] = userinfo
            
            # After successful login → go to main page
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Auth error: {str(e)}")
            session.clear()
            return redirect(url_for('goodbye'))


    @app.route('/logout')
    def logout():
        session.clear()
        
        # Build proper Cognito logout URL
        cognito_domain = os.getenv('COGNITO_AUTHORITY')
        client_id = os.getenv('COGNITO_CLIENT_ID')
        
        # After Cognito logout → go back to goodbye page
        logout_redirect_uri = url_for('goodbye', _external=True)
        
        logout_url = (
            f"{cognito_domain}/logout"
            f"?client_id={client_id}"
            f"&logout_uri={quote(logout_redirect_uri)}"
        )
        
        return redirect(logout_url)


    @app.route('/goodbye')
    def goodbye():
        """Logged out / welcome page with Login button"""
        return render_template('goodbye.html')


def get_user_email():
    user = session.get('user', {})
    return user.get('email', 'Unknown')

'''
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
    redirect_uri = os.getenv('COGNITO_REDIRECT_URI', 'http://localhost:5000/authorize')  # Dynamic redirect URI
    oauth.register(
        name='oidc',
        authority=os.getenv('COGNITO_AUTHORITY'),
        client_id=os.getenv('COGNITO_CLIENT_ID'),
        client_secret=os.getenv('COGNITO_APP_CLIENT_SECRET'),
        server_metadata_url=os.getenv('COGNITO_METADATA_URL'),
        client_kwargs={
            'scope': 'email openid phone',
            'redirect_uri': redirect_uri,
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
        
        redirect_uri = os.getenv('COGNITO_REDIRECT_URI', 'http://localhost:5000/authorize')
        return oauth.oidc.authorize_redirect(
            redirect_uri,
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

    '''