
import numpy as np
import pandas as pd
from scipy.stats import norm


class BlackScholesOption:
    """
    Black-Scholes model for European call option pricing and Greeks.
    """

    def __init__(self, S, K, T, r, sigma):
        self.S = float(S)
        self.K = float(K)
        self.T = float(T)
        self.r = float(r)
        self.sigma = float(sigma)

    def d1(self):
        return (
            np.log(self.S / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T
        ) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def call_price(self):
        d1 = self.d1()
        d2 = self.d2()

        return (
            self.S * norm.cdf(d1)
            - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        )

    def delta(self):
        return norm.cdf(self.d1())

    def gamma(self):
        return norm.pdf(self.d1()) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        # Per 1% change in volatility
        return self.S * norm.pdf(self.d1()) * np.sqrt(self.T) / 100

    def theta(self):
        # Per calendar day
        d1 = self.d1()
        d2 = self.d2()

        theta_annual = (
            -self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
            - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        )

        return theta_annual / 365

    def rho(self):
        # Per 1% change in interest rate
        d2 = self.d2()

        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2) / 100

    def summary(self):
        result = {
            "Option Price": self.call_price(),
            "Delta": self.delta(),
            "Gamma": self.gamma(),
            "Vega": self.vega(),
            "Theta": self.theta(),
            "Rho": self.rho()
        }

        return pd.DataFrame(result, index=["European Call"]).T
