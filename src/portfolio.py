import numpy as np


def simulate_returns(mu, sigma, T, dt=1, seed=None):
    """
    Simulate multiplicative portfolio returns using Geometric Brownian Motion.

    Parameters:
        mu (float): Expected annual return
        sigma (float): Annual volatility (standard deviation)
        T (int or float): Time horizon in years
        dt (float): Time step in years
        seed (int, optional): Random seed for reproducibility

    Returns:
        np.ndarray: Array of multiplicative return factors
    """
    if sigma < 0:
        raise ValueError("Volatility (sigma) must be non-negative")
    if T <= 0:
        raise ValueError("Time horizon (T) must be positive")
    if dt <= 0:
        raise ValueError("Time step (dt) must be positive")

    if seed is not None:
        np.random.seed(seed)

    N = int(T / dt)
    Z = np.random.normal(size=N)

    # Calculate return factors using Geometric Brownian Motion
    returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    return returns