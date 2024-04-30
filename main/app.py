import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = os.getenv('API_KEY', 'AIzaSyAVZhXNtFnRkq0Dzx8WZLTd4hxRo-w98q4')

def check_monetization_eligibility(channel_id):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.channels().list(
            part='snippet,statistics,status',
            id=channel_id
        )
        response = request.execute()

        if 'items' in response and response['items']:
            channel = response['items'][0]
            snippet = channel.get('snippet', {})
            statistics = channel.get('statistics', {})
            
            subscriber_count = int(statistics.get('subscriberCount', 0))

            if subscriber_count >= 1500:
                return f"Channel '{snippet.get('title', '')}' is monetized."
            else:
                return f"Channel '{snippet.get('title', '')}' is not monetized."

    except HttpError as e:
        return f"Error: {e.content}"

def lambda_handler(event, context):
    try:
        # Extracting channel_id from the event
        channel_id = event.get('channel_id')
        
        if not channel_id:
            return {
                'statusCode': 400,
                'body': json.dumps('Channel ID is missing in the request.')
            }

        result = check_monetization_eligibility(channel_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }

if __name__ == '__main__':
    event = {'channel_id': input("Enter YouTube Channel ID: ")}
    context = {}
    print(lambda_handler(event, context))