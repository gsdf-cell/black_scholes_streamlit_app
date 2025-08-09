import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from black_scholes import BlackScholes

#Monte Carlo Simulation
def monte_carlo_option_price(S, K, T, sigma, r, simulations=10000, option_type="call"):
    np.random.seed(42)  # Ensures consistent simulation results
    Z = np.random.standard_normal(simulations)
    ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    if option_type == "call":
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)
    return np.exp(-r * T) * np.mean(payoffs)


#Streamlit Configuration
st.set_page_config(
    page_title = "Black-Scholes Option Pricing",
    page_icon="💰",
    layout = "centered"
)
st.title("📈 Option Pricing Dashboard")
st.markdown("Created by Gurpartap Singh ")

#Sidebar inputs
st.sidebar.header("📊 Model Inputs")
S = st.sidebar.number_input("Current Asset Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Time to Maturity (Years)", value=1.0)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
r = st.sidebar.number_input("Risk-Free Interest Rate (r)", value=0.05)

#Heatmap controls
st.sidebar.subheader("♨️ Heatmap Range")
spot_range_slider = st.sidebar.slider(
    "Spot Price Range (£)",
    min_value = 0.0,
    max_value = 2.0 * S,
    value=(S * 0.8, S * 1.2), # sets initial range values
    step=1.0
)

vol_range_slider = st.sidebar.slider(
    "Volatility Range (σ)",
    min_value = 0.01,
    max_value = 1.0,
    value=(sigma * 0.5, sigma * 1.5),
    step=0.01
)

# Create arrays of values to use for plotting
spot_range = np.linspace(spot_range_slider[0], spot_range_slider[1], 10)
vol_range = np.linspace(vol_range_slider[0], vol_range_slider[1], 10)

#Sidebar inputs for purchase prices
with st.sidebar:
    st.subheader("🎯 Purchase Prices")
    purchase_call = st.number_input("Purchase Price for Call (£)", value = 10.0)
    purchase_put = st.number_input("Purchase Price for Put (£)", value = 10.0)

# Black Scholes and Monte Carlo
# Always calculate Black-Scholes prices for current input
bs = BlackScholes(S, K, T, sigma, r)
call, put = bs.calculate_prices()
pnl_call_single = call - purchase_call #float not an array
pnl_put_single = put - purchase_put

# Monte Carlo estimated prices
monte_carlo_call = monte_carlo_option_price(S, K, T, sigma, r, option_type="call")
monte_carlo_put = monte_carlo_option_price(S, K, T, sigma, r, option_type="put")


# Display the theoretical prices in a styled way
st.markdown("## 💸 Theoretical Option Prices")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📞 Call Option Value", value=f"£{call:.2f}", delta=None)

with col2:
    st.metric(label="🛡️ Put Option Value", value=f"£{put:.2f}", delta=None)

st.markdown("## 🎲 Monte Carlo Simulated Prices")

col_mc1, col_mc2 = st.columns(2)

with col_mc1:
    st.metric(label="📞 Monte Carlo Call Price", value=f"£{monte_carlo_call:.2f}")

with col_mc2:
    st.metric(label="🛡️ Monte Carlo Put Price", value=f"£{monte_carlo_put:.2f}")

st.markdown("### 💡 Current Profit / Loss")
st.write(f"📞 Call P&L: **£{pnl_call_single:.2f}** | 🛡️ Put P&L: **£{pnl_put_single:.2f}**")

# Loop through each combination of spot prices and volatility, creating 2 matrices to show how option price changes
# Empty 2D arrays filled with zeros to store call and put prices
# HeatMap Data
call_prices = np.zeros((len(vol_range), len(spot_range)))
put_prices = np.zeros((len(vol_range), len(spot_range)))

for i, vol in enumerate(vol_range):
    for j, spot in enumerate(spot_range):
        bs_grid = BlackScholes(S=spot, K=K, T=T, sigma=vol, r=r) # creating new instance of pricing model
        call, put = bs_grid.calculate_prices() # calls your model to get call and put prices for that specific combo of vol and spot
        call_prices[i, j] = call # saves it in the correct cell
        put_prices[i, j] = put

#Calculate Profit/Loss matrices
pnl_call = call_prices - purchase_call
pnl_put = put_prices - purchase_put

# HeatMap Charts
# Showing plots in the app
st.subheader("📊 Option Price Heatmaps")
st.write("These heatmaps show how theoretical option prices change based on combinations of spot price and volatility. Darker colours indicate higher prices and lighter colours indicate lower prices. Use the sliders on the left to explore different market scenarios.")

#Call price heat map
fig_call, ax_call = plt.subplots(figsize=(8, 6))
sns.heatmap(call_prices,
            xticklabels=np.round(spot_range, 2),
            yticklabels=np.round(vol_range, 2),
            cmap="YlGnBu", # colour of map
            annot=True, # showing the numbers in the boxes
            fmt=".2f", # decimal points
            ax=ax_call) # tells seaborn which plots to draw on
ax_call.set_title("Call Option Prices")
ax_call.set_xlabel("Spot Price")
ax_call.set_ylabel("Volatility")

# Put Price Heatmap
fig_put, ax_put = plt.subplots(figsize=(8, 6))
sns.heatmap(put_prices,
            xticklabels=np.round(spot_range, 2),
            yticklabels=np.round(vol_range, 2),
            cmap="YlOrRd",
            annot=True,
            fmt=".2f",
            ax=ax_put)
ax_put.set_title("Put Option Prices")
ax_put.set_xlabel("Spot Price")
ax_put.set_ylabel("Volatility")

st.pyplot(fig_call)
st.pyplot(fig_put)

st.subheader("💰 Profit & Loss Heatmaps")

st.write("""
These P&L Heatmaps show how much profit or loss you would make depending on different market conditions.
They're calculated by comparing the model price with your purchase price:

**P&L = Model Price - Purchase Price**

- Green = profit  
- Yellow = break-even  
- Red = loss  

Adjust the 'Purchase Prices' to the left in the sidebar to see how it affects your profit or loss.
""")

#Call P&L Heatmap
fig_pnl_call, ax_pnl_call = plt.subplots(figsize=(8, 6))
sns.heatmap(pnl_call,
            xticklabels=np.round(spot_range, 2),
            yticklabels=np.round(vol_range, 2),
            cmap="RdYlGn",
            center=0,  # So yellow is at 0
            annot=True,
            fmt=".2f",
            ax=ax_pnl_call)
ax_pnl_call.set_title("Call Option P&L (£)")
ax_pnl_call.set_xlabel("Spot Price")
ax_pnl_call.set_ylabel("Volatility")

#Put P&L Heatmap
fig_pnl_put, ax_pnl_put = plt.subplots(figsize=(8, 6))
sns.heatmap(pnl_put,
            xticklabels=np.round(spot_range, 2),
            yticklabels=np.round(vol_range, 2),
            cmap="RdYlGn",
            center=0,
            annot=True,
            fmt=".2f",
            ax=ax_pnl_put
            )
ax_pnl_put.set_title("Put Option P&L (£)")
ax_pnl_put.set_xlabel("Spot Price")
ax_pnl_put.set_ylabel("Volatility")

st.pyplot(fig_pnl_call)
st.pyplot(fig_pnl_put)

st.subheader("📉 P&L Line Charts at Expiry")
st.write("These line charts show profit or loss if you held the option until expiry. The red dashed line marks the strike price, and the point where the line crosses zero shows your break-even.")
spot_prices = np.linspace(60, 140, 100)
# Calculate theoretical profit or loss if you exercised the option at expiry
call_payoffs = np.maximum(spot_prices - K, 0) - purchase_call
put_payoffs = np.maximum(K - spot_prices, 0) - purchase_put

# Line plot for Call Option P&L
fig_line_call, ax_line_call = plt.subplots(figsize=(8, 6))
ax_line_call.plot(spot_prices, call_payoffs, label="Call P&L", color="blue")
ax_line_call.axhline(0, color='black', linestyle='--') # draw dashed black line at y=0
ax_line_call.axvline(K, color='red', linestyle='--', label="Strike Price") #draw a vertical line at x=k
ax_line_call.set_title("📞 Call Option P&L at Expiry")
ax_line_call.set_xlabel("Spot Price at Expiry (£)")
ax_line_call.set_ylabel("Profit / Loss (£)")
ax_line_call.legend() # small box (legend box) to explain what each of the different parts of the graph mean

# Line plot for Put Option P&L
fig_line_put, ax_line_put = plt.subplots(figsize=(8, 6))
ax_line_put.plot(spot_prices, put_payoffs, label="Put P&L", color="green")
ax_line_put.axhline(0, color='black', linestyle='--')
ax_line_put.axvline(K, color='red', linestyle='--', label="Strike Price")
ax_line_put.set_title("🛡️ Put Option P&L at Expiry")
ax_line_put.set_xlabel("Spot Price at Expiry (£)")
ax_line_put.set_ylabel("Profit / Loss (£)")
ax_line_put.legend()

st.pyplot(fig_line_call)
st.pyplot(fig_line_put)
