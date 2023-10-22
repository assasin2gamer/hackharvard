import tkinter as tk
import threading
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import csv
import random
import time
from pylsl import StreamInlet, resolve_stream
import pickle
import base64

import firebase_admin
from firebase_admin import credentials, db
import random
from pybloom_live import BloomFilter
import mne


import hashlib
import string

def generate_random_string(row):
    filter = BloomFilter(capacity=100, error_rate=.1)
    for stuff in row:
        filter.add(stuff)
    filter_bytes = pickle.dumps(filter)

    # Convert byte string to Base64 and then decode to ASCII string
    filter_base64 = base64.b64encode(filter_bytes).decode('ascii')

    # Replace non-letter characters to get only letters
    only_letters_string = filter_base64.replace('+', 'X').replace('/', 'Y').replace('=', 'Z')
    return only_letters_string
    #to turn back loaded_filter = pickle.loads(filter_bytes)



# Global variables
current_label = 1
label_var = None
sample_data = []
is_running = True

count = 0
temp_data = []

cred = credentials.Certificate("C:/fuck u who uses onedrive/hackharvard-master/hackharvard-master/examples/auth.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fjo2039mfnbn-default-rtdb.firebaseio.com/'  # Replace with your database URL
})

 # Replace 'path/to/collection' with your desired path




def collect(row):
    global count
    global temp_data
    global ref
    

    
    if count < 100:
       
        count = count + 1
        temp_data.append(row)

    else:
        #send
        bloom = generate_random_string(row)
        ref = db.reference("/data/" + bloom) 
        ref.push(temp_data)


        print("sent")
        time.sleep(1)
        df = pd.DataFrame(temp_data, columns=['cn1', 'cn2', 'cn3', 'cn4', 'cn5', 'cn6', 'cn7', 'cn8', 'cn9', 'cn10', 'cn11', 'cn12', 'cn13', 'cn14', 'cn15'])
        features_list = []


        for column in df.columns:
            # 1. Mean
            mean_val = df[column].mean()

            # 2. Standard deviation
            std_val = df[column].std()

            # 3. Trend (using linear regression)
            trend_val = np.polyfit(df.index, df[column], 1)[0]  # Take the slope of the linear fit

            # 4. Max value
            max_val = df[column].max()

            # 5. Min value
            min_val = df[column].min()

            # Append features to the list
            features_list.append([mean_val, std_val, trend_val, max_val, min_val])

        # Convert features to a DataFrame
        #features_df = pd.DataFrame(features_list, columns=['mean', 'std', 'trend', 'max', 'min'], index=df.columns)
        count = 0
        temp_data = []
        ref = db.reference("/features/" + bloom) 
        ref.push(str(features_list))


def handle_consecutive_ones(row):
    global consecutive_one_counter
    if "one" in row:
        consecutive_one_counter += 1
    else:
        consecutive_one_counter = 0  # Reset the counter if a different value is encountered

    if consecutive_one_counter == 20:
        print("1")
        consecutive_one_counter = 0  # Reset the counter after calling the function

def save_to_csv(sample, label):
    with open('numbers10.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the sample data along with the label to the CSV file
        row = [label] + list(sample)
        csv_writer.writerow(row)
        collect(row)
        
        handle_consecutive_ones(row)  # Check for consecutive occurrences of "one"

def switch_label():
    global current_label
    current_label = random.randrange(10)
    label_var.set(current_label)

def label_switch_timer():
    while is_running:
        switch_label()
        window.update()
        time.sleep(5)

def collect_eeg_data():
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])

    while is_running:
        sample, _ = inlet.pull_sample()
        label = current_label  # Save the current label
        sample_data.append((label, sample))

        # Call save_to_csv to save the sample with the label
        save_to_csv(sample, label)

        # Extract the data for the 16 channels
        eeg_data = np.array(sample)
        if eeg_data.ndim == 1:  # Check if the array is 1D
            eeg_data = eeg_data[:, np.newaxis]  # Reshape the 1D array to a 2D array with a single column
            print(f"Reshaped eeg_data: {eeg_data.shape}")

        # Define parameters for peak detection
        threshold = 5000  # Adjust this based on your data and noise levels
        distance = 500  # Adjust this based on the expected minimum distance between blinks

        # Function to detect peaks (eye blinks) in the signal
        def detect_blinks(signal):
            peaks, _ = find_peaks(signal, height=threshold, distance=distance)
            return peaks

        # Detect eye blinks for each channel
        if len(eeg_data.shape) > 1:
            for channel_index in range(eeg_data.shape[1]):
                channel_data = eeg_data[:, channel_index]
                peaks = detect_blinks(channel_data)
                print(f"Detected {len(peaks)} blinks in channel {channel_index + 1}")
                print(len(peaks))
        else:
            print("Invalid shape of eeg_data. Expected 2D array.")

def stop_threads():
    global is_running
    is_running = False

def main():
    global label_var
    global window
    window = tk.Tk()
    window.title('EEG Data Annotation')
    window.geometry("400x600")

    label_var = tk.StringVar()
    label_var.set(current_label)
    label = tk.Label(window, textvariable=label_var, font=('Helvetica', 96))
    label.pack(fill='both', expand=True)

    label_thread = threading.Thread(target=label_switch_timer)
    label_thread.daemon = True
    label_thread.start()

    eeg_thread = threading.Thread(target=collect_eeg_data)
    eeg_thread.daemon = True
    eeg_thread.start()

    window.protocol("WM_DELETE_WINDOW", stop_threads)  # To handle window close event
    window.mainloop()

if __name__ == '__main__':
    main()
