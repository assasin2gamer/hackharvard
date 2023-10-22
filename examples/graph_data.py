import tkinter as tk
import threading
from pylsl import StreamInlet, resolve_stream
import time
# Constants
MAX_DATA_POINTS = 50
UPDATE_INTERVAL = 200

# Create a list to hold EEGGraph instances
eeg_graphs = []

class EEGGraph(tk.Canvas):
    def __init__(self, master, channel_name, width, height):
        super().__init__(master, width=width, height=height, bg="white")
        self.channel_name = channel_name
        self.data_buffer = [0] * MAX_DATA_POINTS
        self.x_scale = width / (MAX_DATA_POINTS + 1)
        self.y_scale = height / 1000
        self.height = height

    def update_plot(self, new_data):
        self.data_buffer.append(new_data)
        if len(self.data_buffer) > MAX_DATA_POINTS:
            self.data_buffer.pop(0)

        max_value = max(self.data_buffer)*1.0001
        min_value = min(self.data_buffer)*0.9999

        # Calculate the y_scale based on the height of the graph and the data range
        self.y_scale = self.height / (max_value - min_value)

        self.delete("all")

        for i in range(1, len(self.data_buffer)):
            x1 = (i - 1) * self.x_scale
            y1 = self.height - (self.data_buffer[i - 1] - min_value) * self.y_scale
            x2 = i * self.x_scale
            y2 = self.height - (self.data_buffer[i] - min_value) * self.y_scale
            self.create_line(x1, y1, x2, y2, fill="blue")

        self.after(UPDATE_INTERVAL, self.update_plot, new_data)

# Function for the main graph window
def graph_thread():
    root = tk.Tk()
    root.title('EEG Graphs')
    root.geometry("800x600")

    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    channel_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

    # Create EEGGraph instances for each channel
    for name in channel_names:
        width, height = 800, 35
        graph = EEGGraph(frame, name, width, height)
        graph.pack(fill=tk.BOTH, expand=True)
        eeg_graphs.append(graph)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()

# Function for updating the data
def main_thread():
    global inlet
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])

    while True:
        data = inlet.pull_sample()[0]
        for i, graph in enumerate(eeg_graphs):
            graph.update_plot(data[i])
            time.sleep(.001)
        time.sleep(1)

# Create a thread for the main graph window
graph_thread = threading.Thread(target=graph_thread)

# Create a thread for data updating
main_thread = threading.Thread(target=main_thread)

# Start both threads
graph_thread.start()
main_thread.start()
