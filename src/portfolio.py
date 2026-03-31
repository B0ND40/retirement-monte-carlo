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

	returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
	return returns

if __name__ == "__main__":
	r = simulate_returns(0.05, 0.15, 30, seed=42)
	print(r)

