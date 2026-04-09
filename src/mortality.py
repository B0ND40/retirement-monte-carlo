import numpy as np

def simulate_lifespan(mean=85, std=10, min_age=65):

	"""
	Simulate a lifespan using a normal distribution.

	Parameters:
		mean (float): average lifespan
		std (float): standard deviation
		min_age (int): minimum age (e.g., retirement age)

	Returns:
		int: simulated age at death
	"""

	age = np.random.normal(mean, std)
	return max(min_age, int(age))

if __name__ == "__main__":
	for _ in range(5):
		print(simulate_lifespan())


