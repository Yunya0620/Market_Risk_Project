
import pandas as pd
import numpy as np


class HistoricalVaREngine:
    """
    Module 4: Historical Value-at-Risk Engine

    This class calculates one-day Historical VaR using the left tail
    of historical portfolio returns.

    VaR is a one-tail downside risk measure.
    """

    def __init__(
        self,
        portfolio_returns,
        portfolio_value,
        confidence_levels: list = [0.95, 0.99]
    ):
        if isinstance(portfolio_returns, pd.DataFrame):
            self.portfolio_returns = portfolio_returns.iloc[:, 0].copy()
        else:
            self.portfolio_returns = portfolio_returns.copy()

        if isinstance(portfolio_value, pd.DataFrame):
            self.portfolio_value = portfolio_value.iloc[:, 0].copy()
        else:
            self.portfolio_value = portfolio_value.copy()

        self.confidence_levels = confidence_levels
        self.current_portfolio_value = self.portfolio_value.iloc[-1]

        self._validate_inputs()

    def _validate_inputs(self):
        if self.portfolio_returns.empty:
            raise ValueError("Portfolio returns are empty.")

        if self.portfolio_value.empty:
            raise ValueError("Portfolio value series is empty.")

        if self.current_portfolio_value <= 0:
            raise ValueError("Current portfolio value must be positive.")

    def calculate_historical_var(self) -> pd.DataFrame:
        """
        Calculate one-tail Historical VaR.

        For 95% VaR:
        - Use the 5th percentile of historical portfolio returns.

        For 99% VaR:
        - Use the 1st percentile of historical portfolio returns.

        This is left-tail risk because we are looking at the most negative returns.
        """

        results = []

        for confidence_level in self.confidence_levels:
            tail_probability = 1 - confidence_level

            # One-tail left-tail return threshold
            var_return = self.portfolio_returns.quantile(tail_probability)

            # Convert negative return into positive dollar loss
            var_amount = -var_return * self.current_portfolio_value

            results.append({
                "Confidence Level": confidence_level,
                "Tail Probability": tail_probability,
                "VaR Return Threshold": var_return,
                "VaR Amount": var_amount
            })

        return pd.DataFrame(results)

    def calculate_tail_observations(self, confidence_level: float = 0.95) -> pd.DataFrame:
        """
        Return only the left-tail observations used to understand VaR.

        Example:
        For 95% VaR, this returns returns below the 5th percentile.
        """

        tail_probability = 1 - confidence_level
        var_return = self.portfolio_returns.quantile(tail_probability)

        tail_returns = self.portfolio_returns[
            self.portfolio_returns <= var_return
        ].sort_values()

        tail_df = pd.DataFrame({
            "Portfolio Return": tail_returns,
            "Estimated Loss": -tail_returns * self.current_portfolio_value
        })

        return tail_df

    def calculate_worst_historical_days(self, n: int = 10) -> pd.DataFrame:
        """
        Show the worst historical portfolio return days.
        These are the most negative returns, so this is also left-tail.
        """

        worst_returns = self.portfolio_returns.sort_values().head(n)

        worst_days = pd.DataFrame({
            "Portfolio Return": worst_returns,
            "Estimated Loss": -worst_returns * self.current_portfolio_value
        })

        return worst_days

    def calculate_latest_pnl(self, n: int = 10) -> pd.DataFrame:
        """
        Show recent daily portfolio return and estimated PnL.

        This is NOT VaR.
        It is only for checking recent portfolio movement.
        """

        latest_returns = self.portfolio_returns.tail(n)

        latest_pnl = pd.DataFrame({
            "Portfolio Return": latest_returns,
            "Estimated PnL": latest_returns * self.current_portfolio_value
        })

        return latest_pnl

    def run(self) -> dict:
        var_table = self.calculate_historical_var()
        worst_days = self.calculate_worst_historical_days(n=10)
        tail_95 = self.calculate_tail_observations(confidence_level=0.95)
        tail_99 = self.calculate_tail_observations(confidence_level=0.99)
        latest_pnl = self.calculate_latest_pnl(n=10)

        return {
            "var_table": var_table,
            "worst_days": worst_days,
            "tail_95": tail_95,
            "tail_99": tail_99,
            "latest_pnl": latest_pnl,
            "current_portfolio_value": self.current_portfolio_value
        }
