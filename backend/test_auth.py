import firebase_admin
from firebase_admin import auth, credentials
import requests
import os

# 1. Initialize (Make sure path is correct)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def get_test_token(uid="test-user-123"):
    # 1. Generate the custom token (This returns bytes)
    custom_token_bytes = auth.create_custom_token(uid)
    
    # 2. Convert bytes to string
    custom_token_str = custom_token_bytes.decode('utf-8')
    
    API_KEY = "AIzaSyAYAQBgcqi9gIipwowmFQGrKG2LJbznaq0"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}"
    
    data = {"token": custom_token_str, "returnSecureToken": True}
    res = requests.post(url, json=data)
    
    if res.status_code != 200:
        # This will tell us the EXACT reason (e.g., "INVALID_API_KEY")
        print(f"❌ Google Says: {res.json()}") 
        res.raise_for_status()
        
    return res.json()['idToken']
    
def test_django_sync(token):
    """Sends the token to your Django endpoint."""
    url = "http://127.0.0.1:8000/api/users/sync/"
    payload = {"idToken": token}
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    try:
        token = get_test_token()
        print("✅ Obtained Firebase ID Token.")
        test_django_sync(token)
    except Exception as e:
        print(f"❌ Error: {e}")