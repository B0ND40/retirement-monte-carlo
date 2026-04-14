from src.portfolio import simulate_returns
from src.mortality import simulate_lifespan
from src.withdrawal import fixed_withdrawal

def run_simulation(initial_balance=1_000_000, mu=0.05, sigma=0.15, withdrawal=80_000, start_age=65):

    """
    Runs a single simulation of retirement portfolio sustainability.

    Returns:
        bool: True if ruin occurs, False otherwise.
    """
# Step 1: Simulate lifespan
    lifespan = simulate_lifespan(start_age)
    years = lifespan - start_age

    if years <= 0:
        return False # No retirement years, so no risk of ruin

# Step 2: Simulate portfolio returns
    returns = simulate_returns(mu, sigma, years)

# Step 3: Initialize the portfolio
    balance = initial_balance

# Step 4: Simulate each year of retirement
    for r in returns:
        balance *= r
        balance = fixed_withdrawal(balance, withdrawal)

        if balance <= 0:
            return True # Ruin occurs
    return False # Survived through retirement years without ruin

def monte_carlo(num_simulations=10000):
    """
    Runs multiple simulations and estimates the probability of ruin.

    Returns:
        float: estimated probability of ruin.
    """
    ruin_count = 0
    for i in range(num_simulations):
        if run_simulation():
            ruin_count += 1
    return ruin_count / num_simulations

if __name__ == "__main__":
    probability_of_ruin = monte_carlo()
    print(f"Estimated Probability of Ruin: {probability_of_ruin:.2%}")

