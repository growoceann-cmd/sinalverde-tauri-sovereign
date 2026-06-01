from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# Armazenamento em memória (Soberano - Idealmente Redis para escala)
sessions = {}

@app.route('/session/create', methods=['POST'])
def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'status': 'pending', 'data': {}}
    return jsonify({'session_id': session_id})

@app.route('/session/status/<session_id>', methods=['GET'])
def get_status(session_id):
    session = sessions.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify(session)

@app.route('/pair', methods=['POST'])
def pair_device():
    data = request.json
    session_id = data.get('session_id')
    if session_id in sessions:
        sessions[session_id]['status'] = 'authenticated'
        sessions[session_id]['data'] = data.get('device_info', {})
        return jsonify({'message': 'Pairing successful'})
    return jsonify({'error': 'Invalid session'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
