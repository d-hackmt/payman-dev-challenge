# PAYMAN DEV CHALLENGE 

![image](https://github.com/user-attachments/assets/43239be3-e8d3-440f-a115-a155145f23d1)


please feel free to try and contribute : https://tradepay.streamlit.app/

## 🤖 AI-Powered Stock Trader with Payman

This is a **Streamlit-based stock trading demo app** that uses:

- ✅ Real-time stock price data from **Yahoo Finance**
- 📈 Trending stock discovery via **Tavily AI Search**
- 💸 Secure payments using **[Payman.ai](https://payman.ai)** SDK (test rails)
- 🧠 Natural language agent-style commands to handle payments

---

## 🚀 Features

- 🔍 Get **top trending stocks** dynamically via Tavily AI
- 📊 View live **stock prices** using Yahoo Finance
- 🛒 **Buy stocks** in custom quantities and pay using **Payman.ai**
- 💰 Automatically log all purchases with **stop loss** strategy
- 📒 Persistent transaction logs stored in `stock_log.csv`

---

![image](https://github.com/user-attachments/assets/336fc338-fdd7-4870-801b-b8ed49fbf227)


## 🧠 How It Works

1. The app queries Tavily AI for trending stocks (like “Top 5 stocks to invest today”)
2. Fetches current prices via the Yahoo Finance API
3. When a user clicks **Buy**, it:
   - Checks if the payee is created (if not, creates it via Payman)
   - Calculates the total amount (price × quantity)
   - Sends the payment using `PaymanClient.ask()`
   - Logs the transaction with stop loss

---

## 🛠️ Technologies Used

| Component        | Tool / API                |
|------------------|---------------------------|
| Frontend UI      | Streamlit                 |
| Trending Search  | Tavily AI API             |
| Stock Prices     | yFinance (Yahoo Finance)  |
| Payments         | Payman SDK (Natural Lang) |
| Deployment       | Streamlit Cloud           |

---

## 📂 Folder Structure

├── stock_log.csv # Stores purchase history

├── stock.py # Main Streamlit application

├── requirements.txt # Python dependencies

└── secrets.toml # API credentials (not committed)


## 🧪 Test Wallet

All payments are processed on Payman's test rails. No real currency is used.

You can verify transactions using Payman’s .ask("show my last transaction").

## 📦 Installation

```bash

git clone https://github.com/yourusername/ai-stock-trader
pip install -r requirements.txt
streamlit run stock.py
```

## 🤝 Credits

Payman.ai for payment SDK

Tavily AI for trending search

Yahoo Finance for market data

### 📜 License

MIT License. Feel free to fork, modify, and use in your own projects!

