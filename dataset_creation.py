import numpy as np
import pandas as pd
from datetime import datetime

# Function to generate a random price series
def generate_price_series(base_price, trend, seasonality, noise_level, days):
    time = np.arange(days)
    prices = base_price * (1 + trend * time / days) * (1 + seasonality * np.sin(2 * np.pi * time / 365)) 
    noise = np.random.normal(0, noise_level, days)
    return prices + noise

# Set the parameters for random price generation
base_price = np.random.uniform(200, 500)  # Random base price between 200 and 500
trend = np.random.uniform(-0.05, 0.05)  # Random trend between -5% and +5%
seasonality = np.random.uniform(0.1, 0.3)  # Random seasonality effect between 10% and 30%
noise_level = np.random.uniform(5, 20)  # Random noise level between 5 and 20
rows = 351  # Number of rows required

# Set start date and end date
start_date = pd.Timestamp('2010-04-06')
end_date = pd.Timestamp('2017-05-12')

# Generate the full date range between start and end dates
full_date_range = pd.date_range(start=start_date, end=end_date)

# Evenly sample 351 dates between the start and end dates
date_range = np.linspace(0, len(full_date_range) - 1, rows, dtype=int)
date_range = full_date_range[date_range]

# Generate price series for 351 days
prices = generate_price_series(base_price, trend, seasonality, noise_level, rows)

# Create lower and upper bounds for prices
lower_prices = prices * np.random.uniform(0.8, 0.95, len(prices))
upper_prices = prices * np.random.uniform(1.05, 1.2, len(prices))

# Create data for the DataFrame
crop = 'Soya'
data = []
for date, price, lower, upper in zip(date_range, prices, lower_prices, upper_prices):
    data.append({
        'Price_Date': date,
        'Crop': crop,
        'Modal_Price': price,
        'lower_Modal_Price': lower,
        'upper_Modal_Price': upper
    })

# Create DataFrame
df = pd.DataFrame(data)

# Ensure 'Price_Date' is in datetime format
df['Price_Date'] = pd.to_datetime(df['Price_Date'])

# Format 'Price_Date' to show only the year, month, and day
df['Price_Date'] = df['Price_Date'].dt.strftime('%Y-%m-%d')

# Sort by Date and Crop
df = df.sort_values(['Price_Date', 'Crop'])

# Save to CSV with a timestamp to avoid overwriting
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_file = f'soya_{timestamp}.csv'
df.to_csv(csv_file, index=False)

# Display information about the saved CSV file
print(f"CSV file '{csv_file}' has been created successfully.")
print(f"\nDataset shape: {df.shape}")  # Should output (351, 5)
print(f"Date range: {df['Price_Date'].min()} to {df['Price_Date'].max()}")
print(f"Number of crops: {df['Crop'].nunique()}")

# Display first few rows
print("\nFirst few rows of the dataset:")
print(df.head(15).to_string())




