# 'requests' will handle HTTP calls
# 'time' lets us poll via sleep
# 'argparse' takes in user arguments
import requests
import time
import argparse

# Default endpoint for our bots
URL = "https://api.recall.ai/api/v1/bot/"

# Place your API key here
API_TOKEN = "Token <<API_KEY HERE>>"

# Allow user arguments via argparse
#   (required) Meeting link via Zoom's "Copy Invite Link"
#   (optional) Join time for bot in ISO8601 format, bot joins immediately if not provided or in the past
parser = argparse.ArgumentParser(description="Create a bot that joins meetings and provides recording when meeting ends.")
parser.add_argument("meeting", help="Meeting link for bot.")
parser.add_argument("--join-at", help="Specify time (ISO8601) for bot to join meeting.")
args = parser.parse_args()
meeting_url = args.meeting
join_at = args.join_at

# Configure HTTP request
headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}
payload = {
    "meeting_url": meeting_url,
    "join_at": join_at
}

# POST to schedule a bot
response = requests.post(URL, json=payload, headers=headers).json()
print("Bot scheduled.")

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
