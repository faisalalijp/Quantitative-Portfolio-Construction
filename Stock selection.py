import datetime as dt
import pandas as pd
import yfinance as yf
import os
from pandas import ExcelWriter

# Date range for analysis
now = dt.datetime.now()
start = now - dt.timedelta(days=3*365)  # 3 years back from today

def main():
    # Get file path from user input
    file_path = input("Enter the path to your stock list file (CSV or Excel): ").strip()
    if not file_path:
        print("No file provided. Exiting...")
        return

    try:
        # Read stock list
        if file_path.lower().endswith('.csv'):
            stock_list = pd.read_csv(file_path)
        else:
            stock_list = pd.read_excel(file_path)
        if stock_list.empty:
            print("No stocks found in the file.")
            return

        # Prepare export dataframe
        export_list = pd.DataFrame(columns=[  # type: ignore
            'Stock', "50 Day MA", "150 Day MA", 
            "200 Day MA", "52 Week Low", "52 Week High", "Current Price"
        ])

        # Process each stock
        for i, row in stock_list.iterrows():
            stock = str(row["Symbol"]).strip()
            
            # Append .NS if not already present
            if not (stock.endswith('.NS') or stock.endswith('.BO')):
                stock += '.NS'
            
            if not stock or pd.isna(stock):
                continue

            print(f"\nProcessing {stock}...")
            
            try:
                # Download stock data using yfinance directly
                ticker = yf.Ticker(stock)
                df = ticker.history(start=start, end=now)
                if df.empty:
                    print(f"No data available for {stock}")
                    continue

                # Calculate moving averages
                sma_periods = [50, 150, 200]
                for period in sma_periods:
                    df[f"SMA_{period}"] = df["Close"].rolling(window=period).mean().round(2)

                # Get current values
                current_close = df["Close"][-1]
                ma_50 = df["SMA_50"][-1]
                ma_150 = df["SMA_150"][-1]
                ma_200 = df["SMA_200"][-1]
                
                # Calculate 52-week high/low (using 252 trading days)
                one_year = df["Close"][-252:] if len(df) >= 252 else df["Close"]
                low_52week = min(one_year)
                high_52week = max(one_year)
                
                # Get 200 SMA from 20 days ago (1 trading month)
                ma_200_20 = df["SMA_200"][-20] if len(df) >= 20 else 0

                # Check all conditions
                conditions = [
                    current_close > ma_150 > ma_200,  # Condition 1
                    ma_150 > ma_200,                 # Condition 2
                    ma_200 > ma_200_20,              # Condition 3
                    ma_50 > ma_150 > ma_200,         # Condition 4
                    current_close > ma_50,          # Condition 5
                    current_close >= (1.3 * low_52week),  # Condition 6
                    current_close >= (0.75 * high_52week), # Condition 7
                ]
                
                if all(conditions):
                    print(f"{stock} meets all criteria")
                    export_list = pd.concat([export_list, pd.DataFrame([{
                        'Stock': stock,
                        "50 Day MA": ma_50,
                        "150 Day MA": ma_150,
                        "200 Day MA": ma_200,
                        "52 Week Low": low_52week,
                        "52 Week High": high_52week,
                        "Current Price": current_close
                    }])], ignore_index=True)
                else:
                    print(f"{stock} does not meet all criteria")

            except Exception as e:
                print(f"Error processing {stock}: {str(e)}")
                continue

        # Save results
        if not export_list.empty:
            output_dir = os.path.dirname(file_path)
            output_file = os.path.join(output_dir, "ScreenOutput.csv")
            
            export_list.to_csv(output_file, index=False)
            print(f"\nResults saved to: {output_file}")
        else:
            print("\nNo stocks met all the criteria.")

        # Show final results
        print("\nQualified Stocks:")
        print(export_list.to_string(index=False))

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()