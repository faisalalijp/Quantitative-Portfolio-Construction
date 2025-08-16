

# **Quantitative Portfolio Construction**

## 📊 Overview  
This project implements a two-stage quantitative approach to portfolio construction:

1. **Stock Screening** – Filters stocks using technical analysis criteria inspired by Mark Minervini’s trading trends.  
2. **Portfolio Optimization** – Applies Modern Portfolio Theory (Markowitz) to construct optimal portfolios.

---

## 🔍 Methodology

### **Stage 1: Stock Screening**  
Screens stocks based on 7 technical criteria:

- Price > 150-day MA > 200-day MA  
- 150-day MA > 200-day MA  
- Current 200-day MA > 200-day MA from 20 days ago  
- 50-day MA > 150-day MA > 200-day MA  
- Price > 50-day MA  
- Price ≥ 1.3 × 52-week low  
- Price ≥ 0.75 × 52-week high  

**Data Source**: 3 years of historical data from Yahoo Finance  
**Output**: List of qualifying stocks with key metrics

---

### **Stage 2: Portfolio Optimization**  
Implements **Markowitz Mean-Variance Optimization**:

- Calculates expected returns and covariance matrix  
- Runs Monte Carlo simulation (100,000 portfolios)  
- Identifies optimal portfolio with **maximum Sharpe ratio**  
- Visualizes the **efficient frontier**

---

## 🧠 Key Concepts

- **Moving Averages**: 50-day, 150-day, 200-day SMAs  
- **Trend Analysis**: Price relative to moving averages  
- **Markowitz Portfolio Theory**: Risk-return optimization  
- **Efficient Frontier**: Optimal risk-return combinations  
- **Sharpe Ratio**: Risk-adjusted return metric

---

## ⚙️ Dependencies

- Python 3.8+  
- `pandas`  
- `numpy`  
- `yfinance`  
- `matplotlib`

---

Let me know if you'd like help adding usage instructions, sample outputs, or visualizations!
