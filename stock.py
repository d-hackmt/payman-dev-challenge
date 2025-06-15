import streamlit as st
import pandas as pd
import re
import os
import time
from tavily import TavilyClient
import yfinance as yf
from payman_sdk.client import PaymanClient
from payman_sdk.types import PaymanConfig

# === Setup Payman Client ===
PAYMAN_CLIENT_ID = st.secrets["PAYMAN_CLIENT_ID"]
PAYMAN_CLIENT_SECRET = st.secrets["PAYMAN_CLIENT_SECRET"]

config: PaymanConfig = {
    'client_id': PAYMAN_CLIENT_ID,
    'client_secret': PAYMAN_CLIENT_SECRET,
}
client = PaymanClient.with_credentials(config)

# === Tavily Client ===
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# === Purchase Log File ===
LOG_FILE = "stock_log.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["stock", "price", "quantity", "stop_loss", "wallet"]).to_csv(LOG_FILE, index=False)

# === Utilities ===
def get_trending_stocks():
    response = tavily.search("Top trending stocks to invest today ", search_depth="advanced")
    tickers = []
    for snippet in response.get("results", []):
        for word in snippet["content"].split():
            word = re.sub(r'[^A-Za-z]', '', word).upper()
            if 2 <= len(word) <= 5 and word.isalpha():
                tickers.append(word)
    return list(dict.fromkeys(tickers))[:5]

def fetch_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.info.get("regularMarketPrice", None), stock.info.get("shortName", ticker)

def load_log():
    return pd.read_csv(LOG_FILE)

def save_log(df):
    df.to_csv(LOG_FILE, index=False)

# === Streamlit UI ===
st.set_page_config(page_title="AI Stock Trader", layout="centered")
st.title("🤖 AI-Powered Stock Trader with Payman")

wallet_name = "trading"

if st.button("🔍 Get Trending Stocks"):
    tickers = get_trending_stocks()
    st.session_state["tickers"] = tickers

if "tickers" in st.session_state:
    log_df = load_log()
    st.subheader("📈 Trending Stocks")
    for ticker in st.session_state["tickers"]:
        price, name = fetch_stock_price(ticker)
        if price:
            st.markdown(f"### {ticker} - {name}")
            st.write(f"💰 Price: ₹{price}")
            qty = st.number_input(f"Quantity to Buy ({ticker})", min_value=1, value=1, key=f"qty_{ticker}")
            if st.button(f"Buy {ticker}", key=f"buy_{ticker}"):

                # Create payee if not exists
                if ticker not in log_df["stock"].values:
                    try:
                        client.ask(f"create payee {ticker} type test rails")
                        time.sleep(4)
                    except Exception as e:
                        st.error(f"Payee creation failed: {e}")
                        continue

                total_amount = round(price * qty, 2)  # ✅ Ensure clean number
                prompt = f"send {total_amount} TSD to {ticker} type test rails from trading wallet"

                try:
                    client.ask(prompt)
                    time.sleep(2)
                    stop_loss = round(price - 2, 2)
                    new_entry = {"stock": ticker, "price": price, "quantity": qty, "stop_loss": stop_loss, "wallet": "trading"}
                    log_df = pd.concat([log_df, pd.DataFrame([new_entry])], ignore_index=True)
                    save_log(log_df)
                    st.success(f"✅ Purchased {qty} of {ticker} at ₹{price} each. Stop Loss: ₹{stop_loss}")
                except Exception as e:
                    st.error(f"Payment failed: {e}")

    st.markdown("---")
    st.subheader("📒 Purchase Log")
    st.dataframe(load_log())
