import firebase_admin
from firebase_admin import credentials, db

# Initialize the Firebase app
cred = credentials.Certificate("C:/fuck u who uses onedrive/hackharvard-master/hackharvard-master/examples/auth.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fjo2039mfnbn-default-rtdb.firebaseio.com/'  # Replace with your database URL
})

# Reference to the database
ref = db.reference('data')  # Replace 'path/to/collection' with your desired path

# The data you want to send
record = [1,2,3,4,5,6,7,8,9]
# Push the data to Firebase
ref.push(record)

print("Record pushed to Firebase!")