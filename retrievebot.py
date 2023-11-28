# 'requests' will handle HTTP calls
import requests

# Place your API key here
API_TOKEN = "Token <<API_KEY HERE>>"

# Include the bot id in the endpoint
URL = "https://api.recall.ai/api/v1/bot/<<BOT_ID HERE>>/"

# Configure HTTP request
headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}

# GET to retrieve a bot
response = requests.get(URL, headers=headers).json()
print(response)
