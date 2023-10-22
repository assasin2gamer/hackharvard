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
last_highlighted = None
row, col = 0, 0  # Initialize row and col
grid_enabled = False


def save_to_csv(sample, label):
        with open('pixel.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write the sample data along with the label to the CSV file
            row_data = [label] + list(sample)
            csv_writer.writerow(row_data)

def switch_grid():
    global grid_enabled
    global last_highlighted, row, col
    while True:
        if grid_enabled:
            if last_highlighted:
                last_highlighted.configure(bg='white')
            row = random.randint(0, 5)
            col = random.randint(0, 5)
            last_highlighted = cells[row][col]
            last_highlighted.configure(bg='black')
            time.sleep(2)

def collect_eeg_data():
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    global row, col

    while True:
        sample, _ = inlet.pull_sample()
        label = current_label  # Save the current label
        sample_data.append((label, sample))
        save_to_csv(sample, f"({row},{col})")  # You can modify how you want to save this data
def start_grid():
        global grid_enabled
        grid_enabled = True

def main():

    global window, cells, last_highlighted
    window = tk.Tk()
    window.title('EEG Data Annotation')
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry(f"{width}x{height}")
    window.configure(bg='white')

    frame = tk.Frame(window, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    cells = [[None for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            cell = tk.Label(frame, width=10, height=5, relief=tk.RIDGE, bg='white')
            cell.grid(row=i, column=j, padx=2, pady=2)
            cells[i][j] = cell

    grid_thread = threading.Thread(target=switch_grid)
    grid_thread.daemon = True
    grid_thread.start()

    eeg_thread = threading.Thread(target=collect_eeg_data)
    eeg_thread.daemon = True
    eeg_thread.start()

    button = tk.Button(window, text="Start", command=start_grid)
    button.pack(side=tk.TOP, pady=10)

    window.mainloop()

if __name__ == '__main__':
    main()
