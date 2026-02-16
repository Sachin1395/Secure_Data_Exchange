from flask import Flask, jsonify, request
import json
import base64

app = Flask(__name__)

# Dictionary to store encrypted data with access tokens
stored_data = {}

@app.route('/upload/<access_token>', methods=['POST'])
def upload_data(access_token):
    """Endpoint to upload encrypted data"""
    try:
        data = request.get_json()
        stored_data[access_token] = data
        return jsonify({"status": "success", "message": "Data uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/<access_token>', methods=['GET'])
def get_data(access_token):
    """Endpoint to retrieve encrypted data"""
    if access_token in stored_data:
        return jsonify(stored_data[access_token]), 200
    else:
        return jsonify({"error": "Invalid or expired access token"}), 401

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "Server is running"}), 200

if __name__ == '__main__':
    print("\n * * * FLASK SERVER STARTED * * *")
    print(" Server running on http://127.0.0.1:5000/")
    print(" Health check: http://127.0.0.1:5000/health\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
