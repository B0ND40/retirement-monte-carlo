import numpy as np

# Mortality simulation using Gompertz law of mortality
def simulate_lifespan_gompertz(B=5e-6, C=1.08, start_age=65, max_age=110):

	"""
	Simulate a lifespan using the Gompertz law of mortality.

	Parameters:
		B (float): Scale parameter controlling overall mortality level
		C (float): Gompertz exponent (age-dependent increase in mortality)
		start_age (int): age at which to start simulation
		max_age (int): maximum age to simulate

	Returns:
		int: simulated age at death
	"""

	age = start_age

	while age < max_age:
		# Calculate hazard rate at current age
		hazard = B * (C ** age)

		if np.random.rand() < hazard:
			return age # Death occurs at this age
		
		age += 1 # Move to next age

	return max_age # If max age is reached without death, return max age


# Mortality simulation using a simple normal distribution (for comparison)
def simulate_lifespan(mean=85, std=10, start_age=65):

	"""
	Simulate a lifespan using a normal distribution.

	Parameters:
		mean (float): average lifespan
		std (float): standard deviation
		start_age (int): minimum age (e.g., retirement age)

	Returns:
		int: simulated age at death
	"""

	age = np.random.normal(mean, std)
	return max(start_age, int(age))


if __name__ == "__main__":
	N = 10000
	normal = [simulate_lifespan() for _ in range(N)]
	gompertz = [simulate_lifespan_gompertz() for _ in range(N)]

	print("Normal mean: ", np.mean(normal))
	print("Gompertz mean: ", np.mean(gompertz))
	#print("Normal:")
    #for i in range(5):
    #    print(simulate_lifespan())

    #print("\nGompertz:")
    #for i in range(5):
    #    print(simulate_lifespan_gompertz())
