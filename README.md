**Quantitative Portfolio Construction
**
**Overview**

This project implements a two-stage quantitative approach to portfolio construction:

**Stock Screening:** Filters stocks using technical analysis criteria based on Mark Minervini's trading trend

**Portfolio Optimization:** Applies Modern Portfolio Theory (Markowitz) to construct optimal portfolios

**Methodology**
**Stage 1: Stock Screening**
Screens stocks based on **7 technical criteria**:

Price > 150MA > 200MA

150MA > 200MA

Current 200MA > 200MA from 20 days ago

50MA > 150MA > 200MA

Price > 50MA

Price ≥ 1.3×52-week low

Price ≥ 0.75×52-week high

Uses 3 years of historical data from Yahoo Finance

Outputs qualifying stocks with key metrics

**Stage 2: Portfolio Optimization**
Implements Markowitz Mean-Variance Optimization

Calculates expected returns and covariance matrix

Runs Monte Carlo simulation (100,000 portfolios)

Identifies optimal portfolio with maximum Sharpe ratio

Visualizes efficient frontier

****Key Concepts**
****Moving Averages:** 50-day, 150-day, 200-day SMAs

**Trend Analysis** Price relative to moving averages

**Markowitz Portfolio Theory:** Construction of portfolio based on risk-return optimization

**Efficient Frontier:** Optimal risk-return combinations for different protfolio weights

**Sharpe Ratio:** Metric to indicate risk-adjusted return 


Dependencies
Python 3.8+
pandas
numpy
yfinance
matplotlib
