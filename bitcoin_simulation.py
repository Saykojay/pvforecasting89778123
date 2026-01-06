import numpy as np
import pandas as pd

def simulate_bitcoin_prices(days=60, initial_price=50000, seed=123):
    """
    Simulates Bitcoin prices using Geometric Brownian Motion.
    """
    np.random.seed(seed)

    # Parameters for simulation
    # Annual drift (mu) and volatility (sigma)
    mu = 0.5  # 50% annual drift (bull market to encourage golden cross)
    sigma = 0.8  # 80% annual volatility
    dt = 1/365  # Daily time step

    prices = [initial_price]
    for _ in range(days - 1):
        prev_price = prices[-1]
        # Geometric Brownian Motion formula
        drift = (mu - 0.5 * sigma**2) * dt
        shock = sigma * np.sqrt(dt) * np.random.normal()
        price = prev_price * np.exp(drift + shock)
        prices.append(price)

    return prices

def run_simulation():
    days = 60
    prices = simulate_bitcoin_prices(days=days)

    # Create DataFrame
    dates = pd.date_range(start="2023-01-01", periods=days)
    df = pd.DataFrame({'Date': dates, 'Price': prices})

    # Calculate Moving Averages
    df['MA7'] = df['Price'].rolling(window=7).mean()
    df['MA30'] = df['Price'].rolling(window=30).mean()

    # Initialize Portfolio
    initial_cash = 10000
    cash = initial_cash
    btc_holdings = 0
    position = "NEUTRAL" # NEUTRAL, LONG

    ledger = []

    # Trading Loop
    print(f"{'Date':<12} | {'Price':<10} | {'MA7':<10} | {'MA30':<10} | {'Action':<10} | {'Portfolio Value':<15}")
    print("-" * 80)

    for i in range(len(df)):
        date = df.loc[i, 'Date'].strftime('%Y-%m-%d')
        price = df.loc[i, 'Price']
        ma7 = df.loc[i, 'MA7']
        ma30 = df.loc[i, 'MA30']

        action = "HOLD"

        # We need previous day's data to detect crossover
        if i > 0:
            prev_ma7 = df.loc[i-1, 'MA7']
            prev_ma30 = df.loc[i-1, 'MA30']

            # Check if MAs are available (not NaN)
            if not np.isnan(prev_ma7) and not np.isnan(prev_ma30) and \
               not np.isnan(ma7) and not np.isnan(ma30):

                # Golden Cross: 7-day MA crosses ABOVE 30-day MA
                if prev_ma7 <= prev_ma30 and ma7 > ma30:
                    if position != "LONG":
                        # BUY
                        btc_to_buy = cash / price
                        btc_holdings = btc_to_buy
                        cash = 0
                        position = "LONG"
                        action = "BUY"

                # Death Cross: 7-day MA crosses BELOW 30-day MA
                elif prev_ma7 >= prev_ma30 and ma7 < ma30:
                    if position == "LONG":
                        # SELL
                        cash = btc_holdings * price
                        btc_holdings = 0
                        position = "NEUTRAL"
                        action = "SELL"

        current_value = cash + (btc_holdings * price)
        ledger.append({
            'Date': date,
            'Price': price,
            'MA7': ma7,
            'MA30': ma30,
            'Action': action,
            'Value': current_value
        })

        # Handle NaN values for formatting
        ma7_str = f"${ma7:.2f}" if not np.isnan(ma7) else "N/A"
        ma30_str = f"${ma30:.2f}" if not np.isnan(ma30) else "N/A"

        print(f"{date:<12} | ${price:<9.2f} | {ma7_str:<10} | {ma30_str:<10} | {action:<10} | ${current_value:<14.2f}")

    print("-" * 80)

    # Final Performance
    final_value = ledger[-1]['Value']
    profit_loss = final_value - initial_cash
    roi = (profit_loss / initial_cash) * 100

    print("\nFinal Portfolio Performance:")
    print(f"Initial Investment: ${initial_cash:.2f}")
    print(f"Final Value:        ${final_value:.2f}")
    print(f"Profit/Loss:        ${profit_loss:.2f}")
    print(f"ROI:                {roi:.2f}%")

    # Buy and Hold comparison
    initial_btc_price = df.loc[0, 'Price']
    buy_hold_btc = initial_cash / initial_btc_price
    buy_hold_final = buy_hold_btc * df.loc[days-1, 'Price']
    buy_hold_roi = ((buy_hold_final - initial_cash) / initial_cash) * 100

    print(f"Buy & Hold ROI:     {buy_hold_roi:.2f}%")

if __name__ == "__main__":
    run_simulation()
