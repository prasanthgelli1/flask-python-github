from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your GitHub personal access token
REPO_OWNER = 'cleversafe-infra'
REPO_NAME = 'cosautoops'

@app.route('/create_issue', methods=['POST'])
def create_issue():
    try:
        data = request.get_json()

        if not all(key in data for key in ['title', 'description']):
            return jsonify({'error': 'Title and description are required'}), 400

        title = data['title']
        description = data['description']
        ACCESS_TOKEN = data['access_token']

        url = f'https://api.github.ibm.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        payload = {
            'title': title,
            'body': description
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            return jsonify({'message': 'Issue created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create issue'}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
