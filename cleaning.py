import csv
import pandas as pd

def clean_csv(input_file, output_file):
    expected_columns = [
        'user_name', 'user_location', 'user_description', 'user_created',
        'user_followers', 'user_friends', 'user_favourites', 'user_verified',
        'date', 'text', 'hashtags', 'source', 'is_retweet'
    ]
    cleaned_rows = []
    bad_row_count = 0

    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
            header = next(reader)  # Read header
            if header != expected_columns:
                print(f"Warning: Header mismatch. Expected {expected_columns}, got {header}")
            cleaned_rows.append(expected_columns)  # Write standard header

            for i, row in enumerate(reader, start=2):
                try:
                    # Skip rows with incorrect column count
                    if len(row) != 13:
                        print(f"Skipping line {i}: expected 13 fields, saw {len(row)}")
                        bad_row_count += 1
                        continue
                    # Clean fields
                    cleaned_row = []
                    for j, field in enumerate(row):
                        # Replace problematic characters
                        field = field.replace('\n', ' ').replace('\r', ' ').strip()
                        # Escape quotes and commas if needed
                        if j in [2, 9, 10, 11]:  # user_description, text, hashtags, source
                            field = field.replace('"', '\\"').replace(',', '\\,')
                        cleaned_row.append(field)
                    cleaned_rows.append(cleaned_row)
                except Exception as e:
                    print(f"Error processing line {i}: {e}")
                    bad_row_count += 1
                    continue

        # Write cleaned CSV using pandas for proper formatting
        df = pd.DataFrame(cleaned_rows[1:], columns=cleaned_rows[0])
        df.to_csv(output_file, index=False, encoding='utf-8', escapechar='\\', quoting=csv.QUOTE_MINIMAL)
        print(f"Saved cleaned CSV to {output_file}")
        print("Columns:", df.columns.tolist())
        print("Row count:", len(df))
        print("Bad rows skipped:", bad_row_count)
        print("First row:", df.head(1).to_dict())
        print("Sample user_names:", df['user_name'].unique()[:5].tolist())
        print("Sample locations:", df['user_location'].unique()[:5].tolist())

    except FileNotFoundError:
        print(f"{input_file} not found")
    except UnicodeDecodeError:
        print("UTF-8 failed, trying latin1...")
        with open(input_file, 'r', encoding='latin1', errors='replace') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
            header = next(reader)
            cleaned_rows.append(expected_columns)
            for i, row in enumerate(reader, start=2):
                try:
                    if len(row) != 13:
                        print(f"Skipping line {i}: expected 13 fields, saw {len(row)}")
                        bad_row_count += 1
                        continue
                    cleaned_row = []
                    for j, field in enumerate(row):
                        field = field.replace('\n', ' ').replace('\r', ' ').strip()
                        if j in [2, 9, 10, 11]:
                            field = field.replace('"', '\\"').replace(',', '\\,')
                        cleaned_row.append(field)
                    cleaned_rows.append(cleaned_row)
                except Exception as e:
                    print(f"Error processing line {i}: {e}")
                    bad_row_count += 1
                    continue
        df = pd.DataFrame(cleaned_rows[1:], columns=cleaned_rows[0])
        df.to_csv(output_file, index=False, encoding='utf-8', escapechar='\\', quoting=csv.QUOTE_MINIMAL)
        print(f"Saved cleaned CSV to {output_file}")
        print("Columns:", df.columns.tolist())
        print("Row count:", len(df))
        print("Bad rows skipped:", bad_row_count)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_csv('bitcoin_tweets_dataset_2.csv', 'bitcoin_tweets_dataset_2_cleaned.csv')