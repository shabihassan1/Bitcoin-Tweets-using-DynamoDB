import pandas as pd

try:
    df = pd.read_csv('bitcoin_tweets_dataset_2_cleaned.csv', encoding='utf-8', nrows=50000)
    df.to_csv('bitcoin_tweets_dataset_2_subset.csv', index=False, encoding='utf-8')
    print("Created bitcoin_tweets_dataset_2_subset.csv with 50,000 rows")
    print("Columns:", df.columns.tolist())
    print("First row:", df.head(1).to_dict(orient='records')[0])
except Exception as e:
    print(f"Error: {e}")