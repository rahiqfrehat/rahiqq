from flask import Flask, request, jsonify, abort

app = Flask(__name__)
missions = []
mission_counter = 1  

def find_mission_by_id(mission_id):
    return next((mission for mission in missions if mission['id'] == mission_id), None)
@app.route('/missions', methods=['POST'])
def create_mission():
    global mission_counter
    data = request.get_json()
    if not data or 'name' not in data or 'status' not in data:
        abort(400, description="Missing required fields: name and status")
        mission = {
        'id': mission_counter,
        'name': data['name'],
        'status': data['status']
    }
    missions.append(mission)
    mission_counter += 1
    return jsonify(mission), 201
@app.route('/missions', methods=['GET'])
def get_missions():
    return jsonify(missions)


@app.route('/missions/<int:id>', methods=['GET'])
def get_mission_by_id(id):
    mission = find_mission_by_id(id)
    if mission is None:
        abort(404, description="Mission not found")
    return jsonify(mission)

@app.route('/missions/<int:id>', methods=['PUT'])
def update_mission_status(id):
    mission = find_mission_by_id(id)
    if mission is None:
        abort(404, description="Mission not found")
    
    data = request.get_json()
    if 'status' not in data:
        abort(400, description="Missing required field: status")
    
    mission['status'] = data['status']
    return jsonify(mission)
@app.route('/missions/<int:id>', methods=['DELETE'])
def cancel_mission(id):
    mission = find_mission_by_id(id)
    if mission is None:
        abort(404, description="Mission not found")
    
    missions.remove(mission)
    return '', 204

# Error handling for bad requests
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

# Error handling for not found
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)