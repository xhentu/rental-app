import firebase_admin
from firebase_admin import auth, credentials
import requests

# 1. Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def get_complete_token(uid="pro-landlord-777"):
    # Add claims to mimic a real Google profile with a phone number
    developer_claims = {
        'phone_number': '+959123456789',
        'picture': 'https://ui-avatars.com/api/?name=Hein+Chanthu&background=random'
    }
    
    # Generate the custom token with the claims
    custom_token = auth.create_custom_token(uid, developer_claims).decode('utf-8')
    
    # Exchange for ID Token
    API_KEY = "AIzaSyAYAQBgcqi9gIipwowmFQGrKG2LJbznaq0" 
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}"
    
    res = requests.post(url, json={"token": custom_token, "returnSecureToken": True})
    
    if res.status_code != 200:
        raise Exception(f"Firebase Exchange Failed: {res.json()}")
        
    return res.json()['idToken']

def sync_to_django(token):
    print("--- 🚀 Syncing Complete Profile to Django ---")
    url = "http://127.0.0.1:8000/api/users/sync/"
    
    payload = {
        "idToken": token,
        "first_name": "Hein",
        "last_name": "Chanthu"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        user = data['user']
        print(f"✅ Success! User ID: {user['id']}")
        print(f"📧 Email: {user['email']}")
        print(f"📱 Phone: {user['phone_number']}")
        print(f"⏰ Last Login: {user.get('last_login')}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        token = get_complete_token()
        sync_to_django(token)
    except Exception as e:
        print(f"💥 Error: {e}")