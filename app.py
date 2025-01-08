from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/api/uupdata', methods=['GET'])
def get_uup_data():
    try:
        with open('uup_data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "uup_data.json not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))