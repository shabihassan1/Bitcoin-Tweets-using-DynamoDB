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

## Project Structure
```
DDE A1/
├── dynamodb_local_latest/    # DynamoDB Local files
├── scripts/
│   ├── clean_csv.py          # Data cleaning script
│   ├── create_subset.py      # Creates 50k row subset
│   ├── create_table.py       # Table creation
│   ├── insert_data.py        # Data insertion
│   └── queries.py            # Query operations
├── docs/
│   ├── design_document.md    # Schema design
│   └── README.md            # This file
├── data/
│   ├── bitcoin_tweets_dataset_2.csv          # Original data
│   ├── bitcoin_tweets_dataset_2_cleaned.csv  # Cleaned data
│   └── bitcoin_tweets_dataset_2_subset.csv   # 50k subset
└── outputs/
    ├── insert_log.txt        # Insertion log
    └── output.txt           # Query results
```

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

## Output
Results are saved in `output.txt` with UTF-8 encoding to properly display:
- Query results
- Execution statistics
- Operation confirmations

## Troubleshooting
- **Unicode Errors**: Use UTF-8 compatible editors
- **DynamoDB Issues**: Ensure Java 8 is installed
- **Query Problems**: Check `insert_log.txt` for data issues
- **Reinserting Data**: Required after deletion operations

## Submission
Package includes:
- All Python scripts
- Design documentation
- Output files
- README (this file)

Zip structure:
```
DDE_A1.zip/
├── scripts/
├── docs/
├── outputs/
└── README.md
```

## License
This project is for academic purposes as part of the Distributed Data Engineering course. Dataset may have its own licensing requirements.
```

Key improvements:
1. Better organization with clear sections
2. More professional presentation
3. Added visual directory structure
4. Clearer installation/usage instructions
5. Better formatting for readability
6. Added license section
7. Improved troubleshooting guidance

The file maintains all your original content while presenting it in a more professional, standardized README format that's easier to navigate.
