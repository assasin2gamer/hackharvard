import tkinter as tk
import threading
from pylsl import StreamInlet, resolve_stream
import csv
import random
import time

# Global variables
current_label = 1
label_var = None
sample_data = []

def save_to_csv(sample, label):
    with open('numbers.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the sample data along with the label to the CSV file
        row = [label] + sample
        csv_writer.writerow(row)

def switch_label():
    global current_label
    current_label = random.randrange(10)
    time.sleep(5)
    label_var.set(current_label)

def label_switch_timer():
    while True:
        switch_label()
        window.update()
        threading.Timer(5, label_switch_timer).start()

def collect_eeg_data():
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])

    while True:
        sample, _ = inlet.pull_sample()
        label = current_label  # Save the current label
        sample_data.append((label, sample))

        # Call save_to_csv to save the sample with the label
        save_to_csv(sample, label)

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

    window.mainloop()

if __name__ == '__main__':
    main()
