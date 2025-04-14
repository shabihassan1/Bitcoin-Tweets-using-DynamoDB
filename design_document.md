# Bitcoin Tweets Database Design

## Table: BitcoinTweets
- **Primary Key**:
  - **Partition Key**: `UserName` (String)
    - Groups tweets by user for Queries 1, 3, 4.
  - **Sort Key**: `Date` (String, ISO format)
    - Orders tweets chronologically.

- **Attributes**:
  - `UserLocation` (String): User’s location.
  - `UserDescription` (String): User bio.
  - `UserCreated` (String): Account creation date.
  - `UserFollowers` (Number): Follower count.
  - `UserFriends` (Number): Following count.
  - `UserFavorites` (Number): Likes count.
  - `UserVerified` (Boolean): Verification status.
  - `Text` (String): Tweet content.
  - `Hashtags` (List<String>): Tweet hashtags.
  - `Source` (String): Tweet platform.
  - `IsRetweet` (Boolean): Retweet status.

## Global Secondary Indexes
1. **LocationDateIndex**:
   - **Partition Key**: `UserLocation` (String)
   - **Sort Key**: `Date` (String)
   - **Projection**: All attributes
   - **Purpose**: Query 2 (tweets by location).
   - **Justification**: Avoids scans for location queries.

2. **UserFollowersDateIndex**:
   - **Partition Key**: `UserName` (String)
   - **Sort Key**: `UserFollowers` (Number)
   - **Projection**: `UserName`, `UserFollowers`, `Text`, `Hashtags`, `Date`
   - **Purpose**: Query 3 (top users) and Query 4 (their tweets).
   - **Justification**: Optimizes follower-based ranking.

## Design Rationale
- **Primary Key**: `UserName` and `Date` enable user-centric and time-ordered queries.
- **Indexes**:
  - `LocationDateIndex` supports Query 2 efficiently.
  - `UserFollowersDateIndex` reduces scan overhead for Queries 3, 4.
- **Query Optimization**:
  - Queries 1, 2, 4 use key or index lookups.
  - Queries 3, 5 involve sorting but minimize attributes.
  - Query 6 scans selectively.
- **Challenges Handled**:
  - Reserved keywords (`Text`, `Date`) used aliases (`#text`, `#date`).
  - Unicode characters in `Text` handled via UTF-8 output.
- **Scalability**: DynamoDB’s partitioning suits large datasets.

This design ensures efficient queries for all access patterns.


