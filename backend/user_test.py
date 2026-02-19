import firebase_admin
from firebase_admin import auth, credentials
import requests

# 1. Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def get_test_token(uid="test-user-123"):
    print(f"--- Generating Token for UID: {uid} ---")
    
    # Generate the custom token
    custom_token_bytes = auth.create_custom_token(uid)
    custom_token_str = custom_token_bytes.decode('utf-8')
    
    # ⚠️ IMPORTANT: Verify this key in Firebase Console > Project Settings
    API_KEY = "AIzaSyAYAQBgcqi9gIipwowmFQGrKG2LJbznaq0" 
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}"
    
    res = requests.post(url, json={"token": custom_token_str, "returnSecureToken": True})
    
    # Check for errors before trying to access ['idToken']
    if res.status_code != 200:
        error_data = res.json()
        error_msg = error_data.get('error', {}).get('message', 'Unknown Error')
        print(f"❌ Google API Error: {error_msg}")
        
        if error_msg == "IDENTITY_TOOLKIT_DISABLED":
            print("👉 Fix: Enable 'Identity Toolkit API' in Google Cloud Console.")
        elif error_msg == "INVALID_API_KEY":
            print("👉 Fix: Check your Web API Key in Firebase Settings.")
            
        raise Exception(f"Firebase Exchange Failed: {error_msg}")
        
    return res.json()['idToken']
    
def test_django_sync(token):
    print("--- Sending to Django ---")
    url = "http://127.0.0.1:8000/api/users/sync/"
    # Note: We match the key 'idToken' expected by your FirebaseSyncView
    payload = {"idToken": token}
    
    try:
        response = requests.post(url, json=payload)
        print(f"Django Status: {response.status_code}")
        print(f"Django Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Is your Django server running? (python manage.py runserver)")

if __name__ == "__main__":
    try:
        token = get_test_token()
        print("✅ Success! Token obtained.")
        test_django_sync(token)
    except Exception as e:
        print(f"💥 Script Stopped: {e}")