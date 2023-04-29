import requests
import json
import base64
import time

# set up Zoom API key and secret
API_KEY = 'your_zoom_api_key_here'
API_SECRET = 'your_zoom_api_secret_here'

# set up meeting ID and access token
meeting_id = 'your_meeting_id_here'
access_token = ''

# generate access token
def generate_token():
    global access_token
    url = 'https://api.zoom.us/v2/users/{}/token'.format(API_KEY)
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(bytes(API_KEY + ':' + API_SECRET, 'utf-8')).decode('utf-8'),
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        access_token = json.loads(response.content)['token']
    else:
        print('Error generating access token:', response.status_code)

# get transcript for meeting
def get_transcript():
    global access_token
    url = 'https://api.zoom.us/v2/meetings/{}/recordings'.format(meeting_id)
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        recordings = json.loads(response.content)['meetings'][0]['recording_files']
        for recording in recordings:
            if recording['recording_type'] == 'audio_transcript':
                transcript_url = recording['download_url']
                transcript_file = requests.get(transcript_url, allow_redirects=True)
                open('transcript.txt', 'wb').write(transcript_file.content)
                print('Transcript saved successfully.')
                return
        print('Transcript not found.')
    elif response.status_code == 401:
        generate_token()
        get_transcript()
    else:
        print('Error getting recordings:', response.status_code)

# generate access token before making API request
generate_token()

# wait for token to become valid
time.sleep(5)

# get transcript for meeting
get_transcript()
