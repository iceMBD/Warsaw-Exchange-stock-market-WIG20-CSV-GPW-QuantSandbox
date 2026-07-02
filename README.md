# Warsaw-Exchange-stock-market-WIG20-CSV-GPW-QuantSandbox
A self-contained, open-source financial sandbox for analyzing companies listed on the WIG20 Warsaw Stock Exchange (GPW) WIG20 index. **No data fetching required**—this repository comes pre-loaded with historical EOD (End of Day) CSV datasets from 1-1-2026 till 7-2-2026 so you can start simulating instantly.

# 📊 WIGBox (or your chosen name)

A self-contained, open-source financial sandbox for analyzing companies listed on the Warsaw Stock Exchange (GPW) WIG20 index. **No data fetching required**—this repository comes pre-loaded with historical EOD (End of Day) CSV datasets so you can start simulating instantly.

## 🚀 Key Features

*   **Batteries Included:** Includes clean, curated historical CSV data for WIG20 constituents right in the repository.
*   **Instant Backtesting:** Test trading strategies (e.g., Moving Averages, RSI) against the included historical data with zero setup.
*   **Monte Carlo Simulations:** Run thousands of randomized price-path trials to forecast potential risk and return profiles.
*   **Interactive Controls:** Tweak volatility, drift, and time horizons directly through a local dashboard to see how different stocks behave.



Format csv:Here is how those fields map out:

260102: Date in YYMMDD format (January 2, 2026).

090000: Time in HHMMSS format (09:00:00 AM, right at the GPW market open).

925.0000: Asset Price.

1: Volume.

0: Open Interest or auxiliary flag.




To Run the Application:

Install dependencies: pip install streamlit pandas numpy plotly

Run the application from your terminal: streamlit run app.py


---------------


# 📬 Custom Data & Contact

If you require historical CSV data for all companies listed on the Warsaw Stock Exchange (GPW), or specific tickers, from 2020 to the present, please send me an email for a custom quote: **[mbd.boox@gmail.com]**
