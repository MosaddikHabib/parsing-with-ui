import sqlite3
import json
import requests

def get_unsent_data_from_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Retrieve rows where sent_to_api is 0
    # query = 'SELECT id, sample_id, json_data FROM astm_data WHERE sent_to_api = 0'
    query = 'json_data FROM astm_data WHERE sent_to_api = 0'
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def format_data(data):
    formatted_data = []
    for row in data:
        formatted_data.append({
            'id': row[0],
            'sample_id': row[1],
            'json_data': json.loads(row[2]),
        })
    return formatted_data

def send_data_to_api(api_url, data):
    payload = {'data': data}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, headers=headers, json=payload)
    return response

def update_sent_status(db_path, ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Update sent_to_api to 1 for the given ids
    query = 'UPDATE astm_data SET sent_to_api = 1 WHERE id IN ({})'.format(','.join('?' for _ in ids))
    cursor.execute(query, ids)
    conn.commit()
    conn.close()

# Example usage
db_path = 'habib07.db'
data = get_unsent_data_from_database(db_path)
formatted_data = format_data(data)

api_url = 'https://alumni.tara.net.bd/api/result/store'
response = send_data_to_api(api_url, formatted_data)

if response.status_code == 200:
    response_data = response.json()
    if response_data.get('success'):
        # Extract the ids of the successfully sent data
        ids = [row[0] for row in data]
        update_sent_status(db_path, ids)

print(response.status_code)
print(response.json())
