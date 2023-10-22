# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app

import firebase_admin
from firebase_admin import credentials, db

from google.cloud import firestore

def on_document_create(data, context):
    doc_id = context.resource.split('/')[-1]
    input_data = data['value']['fields']
    app2 = initialize_app({'databaseURL': 'https://fjo2039mfnbn.firebaseio.com/'})


    record = [1,2,3,4,5,6,7,8,9]
    # Push the data to the second Firebase database
    ref2 = db.reference('data', app=app2)
    ref2.push(record)
    print(f"Data written to the second Realtime Database reference.")




    
