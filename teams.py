import requests
import json
from flask import Flask, request, redirect

app = Flask(__name__)

# set up Teams API credentials
TENANT_ID = 'a9ae9372-c187-4bde-905a-f23d3643f291'
CLIENT_ID = '264e0eac-a312-4c76-8219-3df46fe35c5a'
CLIENT_SECRET = 'pUg8Q~CxFB_MJN_1M9JATJypAO8arM9w_p9X1cOF'
REDIRECT_URI = 'http://localhost:8080/auth/microsoft-teams/callback'

# set up meeting ID
meeting_id = '63b1ba17-96b6-15a7-853c-346e98cc8c78'
# MjYyNzE5MjQ3NDI0LjI2Mi4wLjAuMTY2NTI2MDU5NjE3LjAuMA==.Y29udGFjdDovLzYwYzBhMjktMGEzYi00NmJhLWI2OWMtMDQxZTgyYzhiMmJj@thread.v2
@app.route('/')
def home():
    return 'Welcome to the Teams Transcript app. Visit /login to start the authorization process.'

@app.route('/login')
def login():
    auth_url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&response_mode=query&scope=offline_access%20https%3A%2F%2Fgraph.microsoft.com%2F.default&state=12345'
    return redirect(auth_url)

@app.route('/auth/microsoft-teams/callback')
def handle_auth_code():
    auth_code = request.args.get('code', '')

    if auth_code:
        access_token = exchange_auth_code(auth_code)
        if access_token:
            get_transcript(access_token, meeting_id)
            return "Access token received and meeting details fetched."
        else:
            return "Error obtaining access token.", 400

    return "Error: No authorization code received.", 400


def exchange_auth_code(auth_code):
    url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 400 and 'error' in response.json() and response.json()['error']['code'] == 'AADSTS70000':
        # Request a new authorization code from the authorization server
        new_auth_code = request_new_auth_code()
        
        # Exchange the new authorization code for an access token
        data['code'] = new_auth_code
        response = requests.post(url, headers=headers, data=data)
    
    return response.json()


def get_transcript(access_token, meeting_id):
    url = f'https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting_id}/sessions'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sessions = json.loads(response.content)['value']
        for session in sessions:
            print(f"Session {session['id']} - Organizer: {session['organizer']['user']['displayName']}")
            url = f'https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting_id}/sessions/{session["id"]}/segments'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                segments = json.loads(response.content)['value']
                for segment in segments:
                    if 'isDeleted' in segment and segment['isDeleted'] == True:
                        continue
                    print(f"{segment['participant']['user']['displayName']}: {segment['content']}")
            else:
                print('Error getting segments:', response.status_code)
                print(response.content)
    else:
        print('Error getting sessions:', response.status_code)
        print(response.content)


def exchange_auth_code_with_retry(auth_code, max_retries=3):
    url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'https://graph.microsoft.com/.default'
    }
    for i in range(max_retries):
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400 and 'error' in response.json() and response.json()['error']['code'] == 'AADSTS70000':
            print(f'Authorization code has expired. Retrying ({i+1}/{max_retries})...')
            time.sleep(1)  # wait for a second before retrying
        else:
            response.raise_for_status()
    raise ValueError(f'Failed to exchange authorization code after {max_retries} retries')


if __name__ == '__main__':
    app.run(debug=True, port=8080)

