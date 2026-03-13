import pandas as pd


def load_data(sentiment_path, trades_path):
    """
    Load sentiment and trader datasets
    """

    sentiment = pd.read_csv(sentiment_path)
    trades = pd.read_csv(trades_path)

    return sentiment, trades


def clean_data(sentiment, trades):
    """
    Clean datasets and prepare them for merging
    """

    # Rename columns for easier use
    trades = trades.rename(columns={
        'Account': 'account',
        'Side': 'side',
        'Closed PnL': 'closedPnL',
        'Size USD': 'size_usd',
        'Size Tokens': 'size_tokens',
        'Execution Price': 'execution_price'
    })

    sentiment = sentiment.rename(columns={
        'classification': 'Classification'
    })

    # Convert timestamps
    trades['Timestamp'] = pd.to_datetime(trades['Timestamp'], unit='ms')
    trades['date'] = trades['Timestamp'].dt.date

    sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date

    return sentiment, trades


def merge_data(sentiment, trades):
    """
    Merge datasets by date
    """

    data = pd.merge(
        trades,
        sentiment[['date', 'Classification']],
        on='date',
        how='left'
    )

    return data


def feature_engineering(data):
    """
    Create analysis features
    """

    # Win indicator
    data['win'] = data['closedPnL'] > 0

    # Trades per day
    trades_per_day = data.groupby('date').size()

    # Daily pnl
    daily_pnl = data.groupby('date')['closedPnL'].sum()

    return data, trades_per_day, daily_pnl


if __name__ == "__main__":

    sentiment_path = "data/fear_greed_index.csv"
    trades_path = "data/historical_data.csv"

    sentiment, trades = load_data(sentiment_path, trades_path)

    sentiment, trades = clean_data(sentiment, trades)

    data = merge_data(sentiment, trades)

    data, trades_per_day, daily_pnl = feature_engineering(data)

    print("Processed dataset shape:", data.shape)