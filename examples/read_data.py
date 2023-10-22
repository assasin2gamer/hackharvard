from pylsl import StreamInlet, resolve_stream
import csv

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    # Create and open a CSV file for writing
    with open('eeg_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write a header row to the CSV file
        csv_writer.writerow(['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7','O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'])  # Add more column names as needed

        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()

            # Write the sample data to the CSV file
            csv_writer.writerow(sample)  # Adjust this based on the structure of your sample data

if __name__ == '__main__':
    main()