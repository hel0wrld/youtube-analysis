from googleapiclient.discovery import build
from auth import api_key as key
from time import sleep
from tqdm import tqdm
import pandas as pd

api_key = key

youtube = build('youtube', 'v3', developerKey= api_key)

channel_id = "UC0EWL3FL95mgUPUtlFwu2bw"
frame = []
next_page_token = None
count = 0

while True:
    if count == 4:
        break
    videos_request = youtube.search().list(
        part = 'id',
        channelId = channel_id,
        maxResults = 50,
        order = 'viewCount',
        pageToken = next_page_token
    )

    videos_response = videos_request.execute()
    # print(videos_response['items'][0]['id']['videoId'])

    video_ids = []
    for item in videos_response['items']:
        if 'videoId' in item['id']:
            video_ids.append(item['id']['videoId'])

    for video_id in tqdm(video_ids):
        
        video_request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
        # print(video_id)

        sleep(0.5)
        video_response = video_request.execute()

        vid_snippet = video_response['items'][0]['snippet']
        vid_stats = video_response['items'][0]['statistics']

        entries = {
            'channel_id' : channel_id,
            'video_id' : video_id,
            'publishedAt' : vid_snippet["publishedAt"],
            'title' : vid_snippet["title"],
            'description' : vid_snippet['description'],
            'viewCount' : vid_stats["viewCount"],
            'likeCount' : vid_stats["likeCount"],
            'commentCount' : vid_stats['commentCount'] if "commentCount" in vid_stats else 0
        }

        frame.append(entries)

        if 'nextPageToken' in videos_response:
            next_page_token = videos_response['nextPageToken']
        else:
            break
    count += 1
    print('\n')

frame = pd.DataFrame(frame)
frame.to_csv('indiainmotion-4.csv')

