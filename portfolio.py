import numpy as np

def simulate_returns(mu, sigma, T, dt=1):
	"""
	Simulate returns using Geometric Brownian Motion.

	Parameters:
		mu (float): expected return
		sigma (float): volatility # standard deviation
		T (int): number of years
		dt (float): time step

	Returns:
		np.array: returns path
	"""

N = int(T / dt)
Z = np.random.normal(size=N)

returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
return returns


