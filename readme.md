# Recall.ai Tutorial

A quick and easy tutorial using the power of Recall.ai and Python to create a bot that joins Zoom meetings and provides a recording of the meeting when it ends.

## Preamble

Broadly speaking, there are two types of demos. A "pitch demo" is designed to show off the features of the product and is often a complex application incorporating lots of moving parts. A "teaching demo" shows how to implement said features and can be very basic in terms of code design. Eventually the two types may converge into being roughly similar but the process of how they get to that point is different. Given the role I am interviewing for is focused on the documentation and support side of the product, I thought it would be appropriate for me to create a "teaching demo" and not a "pitch demo". The route I take in the following code fits my overall philosophy on creating educational content. The basics should be as simple and clear as possible to ensure that there are minimal barriers to entry on using the product. This means that I try to avoid requiring specific domain knowledge outside the product unless that knowledge is inherently necessary to move forward. That is why this tutorial currently uses polling instead of webhooks and manually scheduling bots instead of a calendar integration. If this tutorial is further developed, it should definitely expand to include those topics but I think it is very important to start at the beginning.

## Getting Started

We will go through the coding process step-by-step in the README. You can find the end result of our work in the src files.

### Prerequisites

- Recall.ai API Key
- Zoom Account
- Python 3

## Writing Python Code

### Scheduling our first bot

We will be using the 'requests' module to handle our HTTP calls so first let's import that. We will specify the endpoint that we will be using for our bots as well as our API key and meeting link. Make sure that "Token" is part of the API_TOKEN string.

```
import requests

URL= "https://api.recall.ai/api/v1/bot/"
API_TOKEN = "Token <<API_KEY HERE>>"
MEETING_URL = "<<ZOOM MEETING INVITE HERE>>"
```

Now we need to configure our HTTP request to pass along our API key as well as the meeting URL we will be joining.

```
headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}
payload = {
    "meeting_url": MEETING_URL
}
```

With everything configured, it's time to create the bot. Using the "requests" module, POST against our endpoint with our configured request and print the results.

```
response = requests.post(URL, json=payload, headers=headers).json()
print(response)
```

You should now see a bot join your Zoom meeting! Feel free to chat away; when the meeting is finished our bot will generate a recording. Make sure to copy the "id" field you get in your response as we will be using this in the next step. You can find this program in this repo as "createbot.py".

### Retrieving bot information

Our meeting has ended and a recording has been created but where is it? Let's whip something up to retrieve our bot information.

We'll still need "requests" and our Recall.ai API key but we no longer need the meeting URL (it has ended after all) or a payload in our HTTP request.

```
import requests

API_TOKEN = "Token <<API_KEY HERE>>"

headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}
```

However, we do need to change something from our last program. Instead of hitting the same endpoint we used when creating our bot, this time we'll specify the bot id in the path. This can be easily found in the output of our last program as the "id" field. 

```
URL = "https://api.recall.ai/api/v1/bot/<<BOT ID HERE>>/"
```

Finally, we'll GET the bot and print the response.

```
response = requests.get(URL, headers=headers).json()
print(response)
```

The second field should be "video_url" and if you access the link you'll download the recording of the meeting! This output also contains some neat metadata on the meeting so you can reuse this code if you like. You can find this program in this repo as "retrievebot.py".

### Combining creating and retrieving the bot

We have two different programs to create our bot and then get the information. But what if we want to combine the two to automatically get the bot information after the meeting has ended? There are two methods of doing this. Webhooks are a great way for your application to get notified when your bot changes state and are generally considered the best practice for production environments. However, you can also use the concept of polling to simply and quickly implement a check that automatically provides a video link when the meeting has ended.

We'll reuse our createbot code in our new program.

```
import requests

URL = "https://api.recall.ai/api/v1/bot/"
API_TOKEN = "Token <<API_KEY HERE>>"
MEETING_URL = "<<MEETING URL HERE>>"

headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}
payload = {
    "meeting_url": MEETING_URL
}

response = requests.post(URL, json=payload, headers=headers).json()
print("Bot created.")
```

But this time we'll take the response to our POST request and automatically grab the bot id to access our new endpoint.

```
bot_id = response["id"]
bot_url = URL + bot_id
```

There are multiple items that we can use to identify a bot's current state but because our end goal is a video link, we can simply check to see if the field has been populated yet. If it is null, the meeting has not yet ended. We'll check every 60 seconds using "time.sleep" so make sure to include "time" in your imports. Once "video_url" is populated, we'll print to the console.

```
import time

…

video_url = response["video_url"]

while video_url is None:
    print("Meeting in progress.")
    time.sleep(60)
    video_url = requests.get(bot_url, headers=headers).json()["video_url"]

print(video_url)
```

It's not the most elegant solution but now all you have to do is run this program once at the beginning of the meeting and you'll get the video link at the end. You can find this program in this repo as "pollbot.py".

### Accepting user arguments and scheduling in advance

It can be a hassle changing our code to include a new meeting URL each time so let's make it as simple as possible by specifying our meeting via the command line when launching the program. We'll also include a powerful feature, the ability to schedule the bot ahead of time.

First we'll reuse our old code. Notice that we are no longer including the MEETING_URL as a constant variable and we did not include the previous HTTP payload.

```
import requests
import time

URL = "https://api.recall.ai/api/v1/bot/"

API_TOKEN = "Token <<API_KEY HERE>>"

headers = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}

response = requests.post(URL, json=payload, headers=headers).json()

bot_id = response["id"]
bot_url = URL + bot_id
video_url = response["video_url"]

while video_url is None:
    print("Meeting in progress.")
    time.sleep(60)
    video_url = requests.get(bot_url, headers=headers).json()["video_url"]

print(video_url)
```

Now we'll use "argparse" to help us out with the user arguments. After we import it, we'll define the parser itself that will also provide a '-h' help command. Next, we add in a positional argument for our meeting link. We then get the arguments from the user and assign the meeting_url. Finally, we pass the URL into our payload.

```
import argparse

…

parser = argparse.ArgumentParser(description="Create a bot that joins meetings and provides recording when meeting ends.")
parser.add_argument("meeting", help="Meeting link for bot.")
args = parser.parse_args()
meeting_url = args.meeting

payload = {
    "meeting_url": meeting_url
}
```

And that's it! From now on when we run our program, we can provide the meeting link via the command line so we don't have to alter the code. For example `python meetingbot.py "https://us05web.zoom.us/j/85187478289?pwd=kdaux1UUPaai2KDbyb4BV1Sq7Kd85r.1"` will join that link.

But let's do one more thing before finishing up. Instead of manually creating a bot after you start a meeting, you can schedule bots in advance for your meetings to ensure that they are there at the beginning. We'll use our argument parser to easily add this in.

```
parser.add_argument("--join-at", help="Specify time (ISO8601) for bot to join meeting.")
args = parser.parse_args()
meeting_url = args.meeting
join_at = args.join_at

payload = {
    "meeting_url": meeting_url,
    "join_at": join_at
}
```

Now if we specify '- - join-at=2023-11-28T16:00:00-0500' on the command line, our bot will join the specified meeting at 4pm ET on November 28th. This field remains optional; if we do not specify a time or if we put something in the past, the bot will simply be created immediately. You can find this program in this repo as "meetingbot.py".

### Recap

Through the course of this tutorial we learned how to create meeting bots and retrieve their information. We can run our simple program to schedule our bot in advance at any Zoom meeting.
