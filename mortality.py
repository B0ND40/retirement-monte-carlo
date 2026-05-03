import numpy as np


# Mortality simulation using Gompertz law of mortality
def simulate_lifespan_gompertz(
    B=5e-5,
    C=1.08,
    start_age=65,
    max_age=110
	):
    """
    Simulate a lifespan using the Gompertz law of mortality.

    Parameters:
        B (float): Scale parameter controlling overall mortality level
        C (float): Gompertz exponent (age-dependent increase in mortality)
        start_age (int): Age at which to start simulation
        max_age (int): Maximum age to simulate

    Returns:
        int: Simulated age at death
    """

    age = start_age

    while age < max_age:
        # Hazard (death probability this year)
        hazard = B * (C ** age)

        # Safety: ensure hazard is a valid probability
        hazard = min(hazard, 1.0)

        if np.random.rand() < hazard:
            return age

        age += 1

    # If max_age is reached without death
    return max_age


# Mortality simulation using a normal distribution (baseline comparison)
def simulate_lifespan_normal(
    mean=85,
    std=10,
    start_age=65
	):
    """
    Simulate a lifespan using a normal distribution.

    Parameters:
        mean (float): Average lifespan
        std (float): Standard deviation
        start_age (int): Minimum age (e.g., retirement age)

    Returns:
        int: Simulated age at death
    """

    age = np.random.normal(mean, std)
    return max(start_age, int(age))