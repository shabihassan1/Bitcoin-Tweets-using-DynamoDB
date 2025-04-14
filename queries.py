import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import sys
import io

# Set stdout to handle UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Connect to DynamoDB Local with dummy credentials
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-east-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)
table = dynamodb.Table('BitcoinTweets')

# Query 1: All tweets of a user
def get_user_tweets(username):
    try:
        response = table.query(
            KeyConditionExpression=Key('UserName').eq(username)
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error in get_user_tweets: {e}")
        return []

# Query 2: All tweets by users from the same location
def get_tweets_by_location(location):
    try:
        response = table.query(
            IndexName='LocationDateIndex',
            KeyConditionExpression=Key('UserLocation').eq(location)
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error in get_tweets_by_location: {e}")
        return []

# Query 3: Top k users with most followers
def get_top_k_users_by_followers(k):
    try:
        response = table.scan(
            IndexName='UserFollowersDateIndex',
            ProjectionExpression='#uname, UserFollowers',
            ExpressionAttributeNames={'#uname': 'UserName'}
        )
        users = {}
        for item in response.get('Items', []):
            username = item['UserName']
            # Clean username: remove extra chars like parentheses
            username = username.split(' (')[0].strip('@')
            followers = item['UserFollowers']
            if username not in users or followers > users[username]:
                users[username] = followers
        top_users = sorted(users.items(), key=lambda x: x[1], reverse=True)[:k]
        return [user[0] for user in top_users]
    except ClientError as e:
        print(f"Error in get_top_k_users_by_followers: {e}")
        return []

# Query 4: Tweets by top k users with most followers
def get_tweets_by_top_k_users(k):
    try:
        top_users = get_top_k_users_by_followers(k)
        tweets = []
        for user in top_users:
            user_tweets = get_user_tweets(user)
            tweets.extend(user_tweets)
        return tweets
    except ClientError as e:
        print(f"Error in get_tweets_by_top_k_users: {e}")
        return []

# Query 5: Top k tweets with most matching tags
def get_top_k_tweets_by_tags(k):
    try:
        response = table.scan(
            ProjectionExpression='#text, Hashtags',
            ExpressionAttributeNames={'#text': 'Text'}
        )
        tweet_scores = []
        for item in response.get('Items', []):
            hashtags = item.get('Hashtags', [])
            score = len(hashtags)
            text = item.get('Text', '')
            # Replace problematic Unicode chars
            text = ''.join(c if ord(c) < 128 else '?' for c in text)
            tweet_scores.append({
                'Text': text,
                'Hashtags': hashtags,
                'Score': score
            })
        top_tweets = sorted(tweet_scores, key=lambda x: x['Score'], reverse=True)[:k]
        return top_tweets
    except ClientError as e:
        print(f"Error in get_top_k_tweets_by_tags: {e}")
        return []

# Query 6: Delete posts of users with followers less than threshold
def delete_users_below_followers(threshold):
    try:
        response = table.scan(
            ProjectionExpression='#uname, #date, UserFollowers',
            ExpressionAttributeNames={'#uname': 'UserName', '#date': 'Date'}
        )
        deleted_count = 0
        for item in response.get('Items', []):
            if item['UserFollowers'] < threshold:
                table.delete_item(
                    Key={
                        'UserName': item['UserName'],
                        'Date': item['Date']
                    }
                )
                deleted_count += 1
        return deleted_count
    except ClientError as e:
        print(f"Error in delete_users_below_followers: {e}")
        return 0

# Test queries
if __name__ == "__main__":
    try:
        print("Query 1: Tweets by user 'ChefSam'")
        result = get_user_tweets('ChefSam')[:2]
        print([{'UserName': item['UserName'], 'Text': item['Text'][:50] + '...'} for item in result])

        print("\nQuery 2: Tweets from location 'London'")
        result = get_tweets_by_location('London')[:2]
        print([{'UserName': item['UserName'], 'Text': item['Text'][:50] + '...'} for item in result])

        print("\nQuery 3: Top 3 users by followers")
        top_users = get_top_k_users_by_followers(3)
        print(top_users)

        print("\nQuery 4: Tweets by top 3 users")
        result = get_tweets_by_top_k_users(3)[:2]
        print([{'UserName': item['UserName'], 'Text': item['Text'][:50] + '...'} for item in result])

        print("\nQuery 5: Top 3 tweets by hashtag count")
        result = get_top_k_tweets_by_tags(3)
        print([{'Text': item['Text'][:50] + '...', 'Hashtags': item['Hashtags'], 'Score': item['Score']} for item in result])

        print("\nQuery 6: Delete users with < 500 followers")
        deleted_count = delete_users_below_followers(500)
        print(f"Deleted {deleted_count} tweets")

    except UnicodeEncodeError as e:
        print(f"Unicode encoding error: {e}")
        print("Try redirecting output to a file: python queries.py > output.txt")