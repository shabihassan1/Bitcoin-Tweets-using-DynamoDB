import pandas as pd

try:
    df = pd.read_csv('bitcoin_tweets_dataset_2_cleaned.csv', encoding='utf-8', low_memory=False)
    print("Columns:", df.columns.tolist())
    print("Row count:", len(df))
    # Print first row as plain strings to avoid encoding issues
    first_row = df.head(1).to_dict(orient='records')[0]
    print("First row:")
    for key, value in first_row.items():
        print(f"  {key}: {str(value)[:100]}...")  # Truncate for readability
    print("Sample user_names:", df['user_name'].unique()[:5].tolist())
    print("Sample locations:", df['user_location'].unique()[:5].tolist())
except FileNotFoundError:
    print("bitcoin_tweets_dataset_2_cleaned.csv not found")
except Exception as e:
    print(f"Error: {e}")