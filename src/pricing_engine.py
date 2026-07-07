
import pandas as pd
import numpy as np


class PortfolioPricingEngine:
    """
    Module 2: Portfolio Pricing Engine

    This class calculates:
    - Daily position values
    - Total portfolio market value
    - Current market value
    - Daily PnL
    - Daily portfolio returns
    - Cumulative return
    - Current portfolio weights
    """

    def __init__(self, prices: pd.DataFrame, portfolio: pd.DataFrame):
        self.prices = prices.copy()
        self.portfolio = portfolio.copy()

        self.tickers = self.portfolio["Ticker"].tolist()
        self.quantities = self.portfolio.set_index("Ticker")["Quantity"]

        self._validate_inputs()

    def _validate_inputs(self):
        """
        Check that every portfolio ticker exists in the price data.
        """

        missing_tickers = [
            ticker for ticker in self.tickers
            if ticker not in self.prices.columns
        ]

        if missing_tickers:
            raise ValueError(f"Missing price data for: {missing_tickers}")

    def calculate_daily_position_values(self) -> pd.DataFrame:
        """
        Calculate daily market value of each position.

        Position value = price × quantity
        """

        position_values = self.prices[self.tickers].multiply(
            self.quantities,
            axis=1
        )

        return position_values

    def calculate_daily_portfolio_value(self) -> pd.Series:
        """
        Calculate total portfolio value for each day.

        Portfolio value = sum of all position values
        """

        position_values = self.calculate_daily_position_values()
        portfolio_value = position_values.sum(axis=1)

        return portfolio_value

    def calculate_current_market_value(self) -> float:
        """
        Calculate latest total portfolio market value.
        """

        portfolio_value = self.calculate_daily_portfolio_value()
        current_market_value = portfolio_value.iloc[-1]

        return current_market_value

    def calculate_daily_pnl(self) -> pd.Series:
        """
        Calculate daily profit and loss.

        Daily PnL = today's portfolio value - yesterday's portfolio value
        """

        portfolio_value = self.calculate_daily_portfolio_value()
        daily_pnl = portfolio_value.diff().dropna()

        return daily_pnl

    def calculate_portfolio_returns(self) -> pd.Series:
        """
        Calculate daily portfolio returns.

        Portfolio return = today's portfolio value / yesterday's portfolio value - 1
        """

        portfolio_value = self.calculate_daily_portfolio_value()
        portfolio_returns = portfolio_value.pct_change().dropna()

        return portfolio_returns

    def calculate_cumulative_return(self) -> pd.Series:
        """
        Calculate cumulative portfolio return.

        Cumulative return = portfolio value today / initial portfolio value - 1
        """

        portfolio_value = self.calculate_daily_portfolio_value()
        cumulative_return = portfolio_value / portfolio_value.iloc[0] - 1

        return cumulative_return

    def calculate_current_weights(self) -> pd.DataFrame:
        """
        Calculate current portfolio weights.

        Weight = position market value / total portfolio market value
        """

        latest_prices = self.prices[self.tickers].iloc[-1]
        current_position_values = latest_prices * self.quantities
        total_value = current_position_values.sum()

        weights = current_position_values / total_value

        weights_df = pd.DataFrame({
            "Ticker": weights.index,
            "Quantity": self.quantities.values,
            "Latest Price": latest_prices.values,
            "Market Value": current_position_values.values,
            "Weight": weights.values
        })

        return weights_df

    def run(self) -> dict:
        """
        Run full portfolio pricing engine.
        """

        position_values = self.calculate_daily_position_values()
        portfolio_value = self.calculate_daily_portfolio_value()
        current_market_value = self.calculate_current_market_value()
        daily_pnl = self.calculate_daily_pnl()
        portfolio_returns = self.calculate_portfolio_returns()
        cumulative_return = self.calculate_cumulative_return()
        weights = self.calculate_current_weights()

        return {
            "position_values": position_values,
            "portfolio_value": portfolio_value,
            "current_market_value": current_market_value,
            "daily_pnl": daily_pnl,
            "portfolio_returns": portfolio_returns,
            "cumulative_return": cumulative_return,
            "weights": weights
        }
