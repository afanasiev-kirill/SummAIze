import requests
import json
import base64

# set up Teams API credentials
TENANT_ID = 'your_tenant_id_here'
CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'

# set up meeting ID and access token
meeting_id = 'your_meeting_id_here'
access_token = ''

# generate access token
def generate_token():
    global access_token
    url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(TENANT_ID)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = json.loads(response.content)['access_token']
    else:
        print('Error generating access token:', response.status_code)

# get transcript for meeting
def get_transcript():
    global access_token
    url = 'https://graph.microsoft.com/v1.0/meetingTranscripts/{}'.format(meeting_id)
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        transcript = json.loads(response.content)['content']
        open('transcript.txt', 'w').write(transcript)
        print('Transcript saved successfully.')
    elif response.status_code == 401:
        generate_token()
        get_transcript()
    else:
        print('Error getting transcript:', response.status_code)

# generate access token before making API request
generate_token()

# get transcript for meeting
get_transcript()
