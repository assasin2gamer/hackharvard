import tkinter as tk
import threading
from pylsl import StreamInlet, resolve_stream
import csv
import random
import time

# Global variables
current_label = 1
sample_data = []

def save_to_csv(sample, label):
    with open('pixel.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the sample data along with the label to the CSV file
        row_data = [label] + list(sample)
        csv_writer.writerow(row_data)

def switch_grid(window, cells):
    last_highlighted = None
    while True:
        if last_highlighted:
            last_highlighted.configure(bg='white')
        row = random.randint(0, 5)
        col = random.randint(0, 5)
        last_highlighted = cells[row][col]
        last_highlighted.configure(bg='black')
        time.sleep(5)

def collect_eeg_data():
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])

    while True:
        sample, _ = inlet.pull_sample()
        sample_data.append(sample)

def main():
    window = tk.Tk()
    window.title('EEG Data Annotation')
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry(f"{width}x{height}")
    window.configure(bg='white')

    cells = [[None for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            cell = tk.Label(window, width=10, height=5, relief=tk.RIDGE, bg='white')
            cell.grid(row=i, column=j, padx=2, pady=2)
            cells[i][j] = cell

    def start_grid():
        grid_thread = threading.Thread(target=switch_grid, args=(window, cells))
        grid_thread.daemon = True
        grid_thread.start()

    start_button = tk.Button(window, text="Start Grid", command=start_grid)
    start_button.grid(row=7, column=3, pady=20)

    eeg_thread = threading.Thread(target=collect_eeg_data)
    eeg_thread.daemon = True
    eeg_thread.start()

    window.mainloop()

if __name__ == '__main__':
    main()
