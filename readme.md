## Project Overview
This project implements a DynamoDB-based database to store and analyze Bitcoin-related tweets. It demonstrates:
- Data cleaning and preprocessing
- NoSQL database design
- Efficient data ingestion
- Complex query operations

Key features:
- Handles Unicode characters and emojis
- Processes 50,000 tweets efficiently
- Implements optimized global secondary indexes
- Provides analytical queries on tweet data

## Prerequisites
- **Software**:
  - Python 3.12+
  - Java 8 (for DynamoDB Local)
  - DynamoDB Local

- **Python Packages**:
  ```bash
  pip install boto3 pandas
  ```

## Installation
1. Clone/download the project to `C:\Users\shabi\Desktop\DDE A1`
2. Download and extract DynamoDB Local to `C:\Users\shabi\Desktop\DDE A1\dynamodb_local_latest`
3. Place your `bitcoin_tweets_dataset_2.csv` in the project directory

## Usage

### Running the Project
1. Start DynamoDB Local:
   ```bash
   cd C:\Users\shabi\Desktop\DDE A1\dynamodb_local_latest
   java -Djava.library.path=.\DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
   ```

2. In a new terminal, process the data:
   ```bash
   cd C:\Users\shabi\Desktop\DDE A1
   python clean_csv.py
   python create_subset.py
   python create_table.py
   python insert_data.py > insert_log.txt
   python queries.py > output.txt
   ```

### Query Examples
The system executes six analytical queries:
1. Retrieve all tweets by a specific user
2. Find tweets from a specific location
3. Identify top 3 users by follower count
4. Get tweets from top users
5. Find tweets with most hashtags
6. Cleanup: Remove low-follower users


## Database Schema
**Table**: BitcoinTweets  
**Primary Key**: 
- Partition: UserName
- Sort: Date

**Global Secondary Indexes**:
1. LocationDateIndex:
   - Partition: Location
   - Sort: Date
2. UserFollowersDateIndex:
   - Partition: UserName
   - Sort: Followers (descending)


## Troubleshooting
- **Unicode Errors**: Use UTF-8 compatible editors
- **DynamoDB Issues**: Ensure Java 8 is installed
- **Query Problems**: Check `insert_log.txt` for data issues
- **Reinserting Data**: Required after deletion operations
