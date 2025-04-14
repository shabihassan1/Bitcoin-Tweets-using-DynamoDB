import boto3

# Connect to DynamoDB Local with dummy credentials
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-east-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def create_table():
    try:
        table = dynamodb.create_table(
            TableName='BitcoinTweets',
            KeySchema=[
                {'AttributeName': 'UserName', 'KeyType': 'HASH'},
                {'AttributeName': 'Date', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'UserName', 'AttributeType': 'S'},
                {'AttributeName': 'Date', 'AttributeType': 'S'},
                {'AttributeName': 'UserLocation', 'AttributeType': 'S'},
                {'AttributeName': 'UserFollowers', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'LocationDateIndex',
                    'KeySchema': [
                        {'AttributeName': 'UserLocation', 'KeyType': 'HASH'},
                        {'AttributeName': 'Date', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                },
                {
                    'IndexName': 'UserFollowersDateIndex',
                    'KeySchema': [
                        {'AttributeName': 'UserName', 'KeyType': 'HASH'},
                        {'AttributeName': 'UserFollowers', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['Text', 'Hashtags', 'Date']
                    },
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        table.wait_until_exists()
        print("Table created successfully!")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("Table already exists.")

if __name__ == "__main__":
    create_table()