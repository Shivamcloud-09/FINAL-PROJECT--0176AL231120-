import firebase_admin
from firebase_admin import credentials, firestore

# Path to your downloaded service account JSON file
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

db = firestore.client()
