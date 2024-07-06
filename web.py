import serial
import re
import json
import requests

# Serial port settings
serial_port = 'COM13'
baud_rate = 9600

# Open the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# URL of the Django server
server_url = 'http://127.0.0.1:8000/api/data/'

# Function to send ACK
def send_ack():
    ser.write(b'\x06')  # Sending ASCII ACK (0x06)

# Function to receive data from the serial port
def receive_data():
    data = ser.read_until(b'\x04').decode('latin-1').strip()  # Read until EOT (0x04)
    return data

# Function to parse ASTM data
def parse_astm(data):
    # Extract the sample ID
    sample_id_match = re.search(r'O\|\d+\|\d+\^([\w\d]+)\s*\^', data)
    sample_id = sample_id_match.group(1) if sample_id_match else None

    # Extract test results
    test_results = re.findall(r'R\|\d+\|\^\^\^(\d+)/\|([\d\.]+)\|([\w/]+)', data)
    results = [{"test_no": res[0], "result_with_unit": f"{res[1]} {res[2]}"} for res in test_results]

    return {
        "sample_id": sample_id,
        "results": results
    }

# Function to send data to the Django server
def send_data_to_server(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(server_url, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        print("Data sent successfully!")
    else:
        print("Failed to send data. Status code:", response.status_code)

def main():
    current_data = None

    while True:
        received_data = receive_data()
        if received_data:
            parsed_data = parse_astm(received_data)
            print(parsed_data)

            if parsed_data['sample_id']:
                # Store the previous data if there is any
                if current_data:
                    send_data_to_server(current_data)
                # Start new data
                current_data = parsed_data
            else:
                # Ensure current_data is initialized
                if current_data:
                    # Append results to the existing sample data
                    current_data['results'].extend(parsed_data['results'])

            send_ack()

    # Store any remaining data when the loop ends
    if current_data:
        send_data_to_server(current_data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        ser.close()
