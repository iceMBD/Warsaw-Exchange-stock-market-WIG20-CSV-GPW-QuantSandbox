import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from datetime import datetime

st.set_page_config(page_title="WIG20 Quant Sandbox", layout="wide")
st.title("📊 WIG20 Local Quant Sandbox")
st.caption("Backtesting & Monte Carlo Engine for local tick/intraday data")

# 1. Folder Selection Sidebar
st.sidebar.header("📁 Data Source Settings")
folder_path = st.sidebar.text_input("Enter local folder path containing CSVs:", value="./data")

# Helper function to parse the custom date/time format
def load_gpw_data(file_path):
    # Read headerless CSV matching: YYMMDD,HHMMSS,Price,Volume,Flag
    df = pd.read_csv(file_path, header=None, names=["Date", "Time", "Price", "Volume", "Flag"])
    
    # Convert YYMMDD and HHMMSS strings to unified datetime objects
    df['Date'] = df['Date'].astype(str).str.zfill(6)
    df['Time'] = df['Time'].astype(str).str.zfill(6)
    df['Datetime'] = pd.to_datetime(df['Date'] + df['Time'], format='%y%m%d%H%M%S')
    
    df.set_index('Datetime', inplace=True)
    return df.sort_index()

# Check if folder exists and look for CSV files
if os.path.exists(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if csv_files:
        selected_file = st.sidebar.selectbox("Select a WIG20 Company Asset File:", csv_files)
        full_path = os.path.join(folder_path, selected_file)
        
        # Load data safely
        try:
            df = load_gpw_data(full_path)
            st.success(f"Successfully loaded {selected_file} with {len(df)} rows of intraday data.")
            
            # Show raw data snippet
            with st.expander("👀 Preview Loaded CSV Struct"):
                st.dataframe(df.head(10))
                
            # 2. Setup Analysis Tabs
            tab1, tab2 = st.tabs(["📈 Backtesting Strategy", "🎲 Monte Carlo Simulation"])
            
            with tab1:
                st.header("Simple Moving Average (SMA) Backtest")
                fast_ma = st.number_input("Fast SMA Period", min_value=1, value=10)
                slow_ma = st.number_input("Slow SMA Period", min_value=2, value=30)
                
                # Calculate indicators on the transaction Price
                df['Fast_MA'] = df['Price'].rolling(window=fast_ma).mean()
                df['Slow_MA'] = df['Price'].rolling(window=slow_ma).mean()
                
                # Simple Strategy Logic: 1 if Fast > Slow else 0
                df['Signal'] = np.where(df['Fast_MA'] > df['Slow_MA'], 1, 0)
                df['Returns'] = df['Price'].pct_change()
                df['Strategy_Returns'] = df['Returns'] * df['Signal'].shift(1)
                
                # Calculate Cumulative returns
                cum_market = (1 + df['Returns'].fillna(0)).cumprod() - 1
                cum_strategy = (1 + df['Strategy_Returns'].fillna(0)).cumprod() - 1
                
                # Plot performance
                fig_bt = go.Figure()
                fig_bt.add_trace(go.Scatter(x=df.index, y=cum_market, name="Buy & Hold Market"))
                fig_bt.add_trace(go.Scatter(x=df.index, y=cum_strategy, name="SMA Strategy"))
                fig_bt.update_layout(title="Strategy Performance vs Market", yaxis_title="Cumulative Return")
                st.plotly_chart(fig_bt, use_container_width=True)
                
            with tab2:
                st.header("Monte Carlo Future Price Forecasting")
                sim_days = st.slider("Simulation Horizon (Steps ahead)", min_value=10, max_value=500, value=100)
                num_sims = st.slider("Number of Simulation Paths", min_value=10, max_value=500, value=100)
                
                # Derive parameters from historical returns
                log_returns = np.log(df['Price'] / df['Price'].shift(1)).dropna()
                mu = log_returns.mean()
                sigma = log_returns.std()
                
                last_price = df['Price'].iloc[-1]
                
                # Run Geometric Brownian Motion Simulations
                simulation_matrix = np.zeros((sim_days, num_sims))
                for i in range(num_sims):
                    prices = [last_price]
                    for t in range(1, sim_days):
                        # Random shock component
                        shock = np.random.normal(mu, sigma)
                        next_price = prices[-1] * np.exp(shock)
                        prices.append(next_price)
                    simulation_matrix[:, i] = prices
                    
                # Plot Simulation Results
                fig_mc = go.Figure()
                x_axis = np.arange(sim_days)
                for i in range(min(num_sims, 50)): # Cap visualized lines for performance
                    fig_mc.add_trace(go.Scatter(x=x_axis, y=simulation_matrix[:, i], mode='lines', opacity=0.3, showlegend=False))
                    
                fig_mc.update_layout(title=f"Top 50 Monte Carlo Paths for {selected_file}", xaxis_title="Future Step", yaxis_title="Price (PLN)")
                st.plotly_chart(fig_mc, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error parsing file. Please ensure it follows the format layout: {e}")
    else:
        st.warning(f"No CSV files found inside folder: '{folder_path}'")
else:
    st.info(f"Please provide a valid local directory path. Current path path state: '{folder_path}' not found.")