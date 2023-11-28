# 'requests' will handle HTTP calls
# 'time' lets us poll via sleep
import requests
import time

# Default endpoint for our bots
URL = "https://api.recall.ai/api/v1/bot/"

# Place your API key and meeting URL here
API_TOKEN = "Token <<API_KEY HERE>>"
MEETING_URL = "<<ZOOM MEETING LINK HERE>>"

# Configure HTTP request
headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}
payload = {
    "meeting_url": MEETING_URL
}

# POST to create a bot
response = requests.post(URL, json=payload, headers=headers).json()
print("Bot created.")

# Get information for our created bot
bot_id = response["id"]
bot_url = URL + bot_id
video_url = response["video_url"]

# Simple polling checking if meeting has ended
# Once meeting ends, video_url is populated
while video_url is None:
    print("Meeting in progress.")
    time.sleep(60)
    video_url = requests.get(bot_url, headers=headers).json()["video_url"]

print(video_url)
