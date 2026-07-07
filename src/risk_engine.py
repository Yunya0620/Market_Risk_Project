
import pandas as pd
import numpy as np


class MarketRiskEngine:
    """
    Module 3: Market Risk Engine

    This class calculates traditional market risk metrics:
    - Asset volatility
    - Correlation matrix
    - Covariance matrix
    - Portfolio volatility
    - Rolling volatility
    - Portfolio return distribution statistics
    """

    def __init__(
        self,
        asset_returns: pd.DataFrame,
        portfolio_returns,
        weights: pd.DataFrame,
        trading_days: int = 252
    ):
        self.asset_returns = asset_returns.copy()
        self.trading_days = trading_days

        # Convert portfolio returns from DataFrame to Series if needed
        if isinstance(portfolio_returns, pd.DataFrame):
            self.portfolio_returns = portfolio_returns.iloc[:, 0].copy()
        else:
            self.portfolio_returns = portfolio_returns.copy()

        self.weights_df = weights.copy()
        self.tickers = self.weights_df["Ticker"].tolist()
        self.weight_vector = self.weights_df.set_index("Ticker")["Weight"]

        self._validate_inputs()

    def _validate_inputs(self):
        """
        Make sure all portfolio tickers exist in the asset return data.
        """

        missing_tickers = [
            ticker for ticker in self.tickers
            if ticker not in self.asset_returns.columns
        ]

        if missing_tickers:
            raise ValueError(f"Missing return data for: {missing_tickers}")

    def calculate_asset_volatility(self) -> pd.DataFrame:
        """
        Calculate daily and annualized volatility for each asset.

        Daily volatility = standard deviation of daily returns
        Annualized volatility = daily volatility × sqrt(252)
        """

        daily_vol = self.asset_returns[self.tickers].std()
        annualized_vol = daily_vol * np.sqrt(self.trading_days)

        vol_df = pd.DataFrame({
            "Ticker": daily_vol.index,
            "Daily Volatility": daily_vol.values,
            "Annualized Volatility": annualized_vol.values
        })

        return vol_df

    def calculate_correlation_matrix(self) -> pd.DataFrame:
        """
        Calculate the correlation matrix of asset returns.
        """

        correlation_matrix = self.asset_returns[self.tickers].corr()
        return correlation_matrix

    def calculate_covariance_matrix(self) -> pd.DataFrame:
        """
        Calculate the annualized covariance matrix.

        Annualized covariance = daily covariance × 252
        """

        daily_covariance = self.asset_returns[self.tickers].cov()
        annualized_covariance = daily_covariance * self.trading_days

        return annualized_covariance

    def calculate_portfolio_volatility(self) -> float:
        """
        Calculate annualized portfolio volatility.

        Portfolio variance = w.T @ covariance_matrix @ w
        Portfolio volatility = sqrt(portfolio variance)
        """

        covariance_matrix = self.calculate_covariance_matrix()

        # Match weight order to covariance matrix columns
        ordered_weights = self.weight_vector.loc[covariance_matrix.columns].values

        portfolio_variance = ordered_weights.T @ covariance_matrix.values @ ordered_weights
        portfolio_volatility = np.sqrt(portfolio_variance)

        return portfolio_volatility

    def calculate_rolling_volatility(self, window: int = 60) -> pd.Series:
        """
        Calculate rolling annualized portfolio volatility.

        Default window = 60 trading days.
        """

        rolling_volatility = (
            self.portfolio_returns
            .rolling(window=window)
            .std()
            * np.sqrt(self.trading_days)
        )

        return rolling_volatility.dropna()

    def calculate_return_distribution_stats(self) -> pd.DataFrame:
        """
        Calculate descriptive statistics for portfolio returns.
        """

        stats = {
            "Mean Daily Return": self.portfolio_returns.mean(),
            "Daily Volatility": self.portfolio_returns.std(),
            "Annualized Return": self.portfolio_returns.mean() * self.trading_days,
            "Annualized Volatility": self.portfolio_returns.std() * np.sqrt(self.trading_days),
            "Minimum Daily Return": self.portfolio_returns.min(),
            "Maximum Daily Return": self.portfolio_returns.max(),
            "Skewness": self.portfolio_returns.skew(),
            "Kurtosis": self.portfolio_returns.kurtosis()
        }

        stats_df = pd.DataFrame(stats, index=["Portfolio"]).T
        stats_df.columns = ["Value"]

        return stats_df

    def run(self) -> dict:
        """
        Run the full market risk engine.
        """

        asset_volatility = self.calculate_asset_volatility()
        correlation_matrix = self.calculate_correlation_matrix()
        covariance_matrix = self.calculate_covariance_matrix()
        portfolio_volatility = self.calculate_portfolio_volatility()
        rolling_volatility = self.calculate_rolling_volatility(window=60)
        return_stats = self.calculate_return_distribution_stats()

        return {
            "asset_volatility": asset_volatility,
            "correlation_matrix": correlation_matrix,
            "covariance_matrix": covariance_matrix,
            "portfolio_volatility": portfolio_volatility,
            "rolling_volatility": rolling_volatility,
            "return_stats": return_stats
        }
