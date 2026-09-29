from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory database to hold our addition records
addition_db = [
    {"id": 1, "num1": 5, "num2": 10, "result": 15}
]

# 1. READ (GET) - Fetch all addition records
@app.route('/addition', methods=['GET'])
def get_records():
    return jsonify(addition_db), 200

# 2. CREATE (POST) - Add two numbers together and save the record
@app.route('/addition', methods=['POST'])
def create_record():
    data = request.get_json()
    if not data or 'num1' not in data or 'num2' not in data:
        return jsonify({"error": "Please provide num1 and num2"}), 400
    
    n1 = int(data['num1'])
    n2 = int(data['num2'])
    
    new_record = {
        "id": len(addition_db) + 1,
        "num1": n1,
        "num2": n2,
        "result": n1 + n2
    }
    addition_db.append(new_record)
    return jsonify(new_record), 201

# 3. UPDATE (PUT) - Edit numbers in an existing record by ID
@app.route('/addition/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    record = next((r for r in addition_db if r['id'] == record_id), None)
    
    if not record:
        return jsonify({"error": "Record not found"}), 404
        
    if 'num1' in data:
        record['num1'] = int(data['num1'])
    if 'num2' in data:
        record['num2'] = int(data['num2'])
        
    record['result'] = record['num1'] + record['num2']
    return jsonify(record), 200

# 4. DELETE (DELETE) - Remove a record by ID
@app.route('/addition/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    global addition_db
    record = next((r for r in addition_db if r['id'] == record_id), None)
    
    if not record:
        return jsonify({"error": "Record not found"}), 404
        
    addition_db = [r for r in addition_db if r['id'] != record_id]
    return jsonify({"message": f"Record {record_id} successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
