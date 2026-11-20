import googleapiclient.discovery
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

youtube_request = youtube.search().list(
    part='snippet',
    q='Tokido vs AngryBird',
    maxResults=10,
    type='video'
)

response = youtube_request.execute()
print(response)

with open('output.json', 'w') as f:
    json.dump(response, f, indent=4)
