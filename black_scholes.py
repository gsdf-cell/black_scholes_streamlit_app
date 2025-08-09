import numpy as np
from numpy import log, sqrt, exp
from scipy.stats import norm 

class BlackScholes:
    def __init__(self, S, K, T, sigma, r):
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r

    def calculate_prices(self):
        d1 = (log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T))
        d2 = d1 - self.sigma * sqrt(self.T)

        call_price = self.S * norm.cdf(d1) - self.K * exp(-self.r * self.T) * norm.cdf(d2)
        put_price = self.K * exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

        return call_price, put_price

