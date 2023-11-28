# 'requests' will handle HTTP calls
import requests

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
print(response)
