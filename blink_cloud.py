import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)
import numpy as np
import pandas as pd
import tsfresh

from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import make_time_series

db = firestore.client()


const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

// Trigger when a new message is added to 'chat' collection
exports.notifyUser = functions.firestore
    .document('chat/{messageId}')
    .onCreate((snapshot, context) => {
        const messageData = snapshot.data();
        const userId = messageData.userId;
        
        // Logic to notify the user about the new message
        // For example, send a push notification or an email

        return null; // Return null to indicate completion of function
    });

    

def trigger_cloud_computation(df):
    # Fetch data from Firebase (assuming a collection named 'data' and document named 'input')
    input_data_ref = db.collection('data').document('input')

    # Convert to long format suitable for tsfresh
    df_long = make_time_series(df, column_id="feature1", column_sort="time")
    extracted_features = extract_features(df_long, column_id="id", column_sort="time")

    # Put the output back to Firebase (assuming a collection named 'data' and document named 'output')
    output_data_ref = db.collection('data').document('output')
    output_data_ref.set({'features': extracted_features})



# how is it triggered
# how is it processed
# where does it go
#
#
#
#please test this code with a test file upload into the original firebase and see if the trigger creates a new entry in the second firebase
#
#
#
#

if __name__ == "__main__":
    trigger_cloud_computation()