from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def connect_to_database():
    connection = sqlite3.connect('habib04.db')
    return connection

# Endpoint to get all data
@app.route('/api/data', methods=['GET'])
def get_data():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM astm_data")
    records = cursor.fetchall()
    data = []
    for record in records:
        data.append({
            "id": record[0],
            "sample_id": record[1],
            "json_data": record[2]
        })
    connection.close()
    return jsonify(data)

# Endpoint to get data by sample_id
@app.route('/api/data/<sample_id>', methods=['GET'])
def get_data_by_sample_id(sample_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM astm_data WHERE sample_id = ?", (sample_id,))
    records = cursor.fetchall()
    data = []
    for record in records:
        data.append({
            "id": record[0],
            "sample_id": record[1],
            "json_data": record[2]
        })
    connection.close()
    return jsonify(data)

# Endpoint to add new data (for testing purposes)
@app.route('/api/data', methods=['POST'])
def add_data():
    sample_id = request.json['sample_id']
    json_data = request.json['json_data']
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO astm_data (sample_id, json_data) VALUES (?, ?)", (sample_id, json_data))
    connection.commit()
    connection.close()
    return jsonify({"message": "Data added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
