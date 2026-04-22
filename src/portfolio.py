import numpy as np

def simulate_returns(mu, sigma, T, dt=1, seed=None):
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
		raise ValueError("Volatility (sigma) must be non-negative") # Added validation for sigma
	if T <= 0:
		raise ValueError("Time horizon (T) must be positive") # Added validation for T
	if dt <= 0:
		raise ValueError("Time step (dt) must be positive") # Added validation for dt

	if seed is not None:
		np.random.seed(seed) # Set seed for reproducibility
	
	N = int(T / dt) # Number of time steps
	Z = np.random.normal(size=N) # Standard normal random variables

	returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z) # Calculate returns using GBM formula
	return returns

# Example usage
if __name__ == "__main__":
	r = simulate_returns(0.05, 0.15, 30, seed=42) 
	print(r)

