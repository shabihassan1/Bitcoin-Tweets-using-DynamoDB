import pandas as pd
import boto3
from botocore.exceptions import ClientError
import ast

# Connect to DynamoDB Local with dummy credentials
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-east-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)
table = dynamodb.Table('BitcoinTweets')

def safe_parse_hashtags(hashtag_str):
    """Safely parse hashtags string to list."""
    try:
        # Handle common cases
        if pd.isna(hashtag_str) or hashtag_str == '' or hashtag_str == '[]':
            return []
        # Try ast.literal_eval for safe parsing
        parsed = ast.literal_eval(hashtag_str)
        if isinstance(parsed, list):
            return [str(tag) for tag in parsed]
        return []
    except (ValueError, SyntaxError):
        # Fallback: split by commas and clean
        return [tag.strip(" '[]") for tag in hashtag_str.split(',') if tag.strip(" '[]")]

def insert_data(csv_file):
    try:
        df = pd.read_csv(csv_file, encoding='utf-8', low_memory=False)
        print(f"Loaded {len(df)} rows from CSV.")
        
        batch_size = 25  # DynamoDB batch write limit
        items = []
        successful_rows = 0
        
        for index, row in df.iterrows():
            try:
                # Prepare item, handling nulls and data types
                item = {
                    'UserName': str(row.get('user_name', '')) or 'unknown_' + str(index),
                    'Date': str(row.get('date', '')) or '1970-01-01 00:00:00',
                    'UserLocation': str(row.get('user_location', 'Unknown')) if pd.notna(row.get('user_location')) else 'Unknown',
                    'UserDescription': str(row.get('user_description', '')) if pd.notna(row.get('user_description')) else '',
                    'UserCreated': str(row.get('user_created', '')) or '1970-01-01 00:00:00',
                    'UserFollowers': int(float(row.get('user_followers', 0))) if pd.notna(row.get('user_followers')) else 0,
                    'UserFriends': int(float(row.get('user_friends', 0))) if pd.notna(row.get('user_friends')) else 0,
                    'UserFavorites': int(float(row.get('user_favourites', 0))) if pd.notna(row.get('user_favourites')) else 0,
                    'UserVerified': str(row.get('user_verified', 'FALSE')).upper() == 'TRUE',
                    'Text': str(row.get('text', '')) if pd.notna(row.get('text')) else '',
                    'Hashtags': safe_parse_hashtags(row.get('hashtags', '[]')),
                    'Source': str(row.get('source', '')) if pd.notna(row.get('source')) else '',
                    'IsRetweet': str(row.get('is_retweet', 'FALSE')).upper() == 'TRUE'
                }
                
                # Skip if key attributes are empty
                if not item['UserName'] or not item['Date']:
                    print(f"Skipping row {index}: Missing UserName or Date")
                    continue
                
                items.append({'PutRequest': {'Item': item}})
                
                # Write batch when full or at end
                if len(items) >= batch_size or index == len(df) - 1:
                    try:
                        dynamodb.batch_write_item(RequestItems={'BitcoinTweets': items})
                        successful_rows += len(items)
                        print(f"Inserted {successful_rows} rows up to index {index}...")
                        items = []  # Clear batch
                    except ClientError as e:
                        print(f"Batch write error at row {index}: {e}")
                        # Retry individually to isolate bad items
                        for item in items:
                            try:
                                dynamodb.batch_write_item(RequestItems={'BitcoinTweets': [item]})
                                successful_rows += 1
                            except ClientError as e:
                                print(f"Failed to insert item at row {index}: {e}")
                        items = []
                
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue
        
        print(f"Data insertion completed! Total successful rows: {successful_rows}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found.")
    except Exception as e:
        print(f"Error loading CSV: {e}")

if __name__ == "__main__":
    insert_data('bitcoin_tweets_dataset_2_subset.csv')