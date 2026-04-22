from src.portfolio import simulate_returns
from src.mortality import simulate_lifespan, simulate_lifespan_gompertz
from src.withdrawal import fixed_withdrawal

def run_simulation(initial_balance=1_000_000, mu=0.05, sigma=0.15, withdrawal=80_000, start_age=65, lifespan_model=None):

    """
    Runs a single simulation of retirement portfolio sustainability.

    Returns:
        bool: True if ruin occurs, False otherwise.
    """
    # Use the specified lifespan model, or default to Gompertz if none provided
    if lifespan_model is None:
        lifespan_model = simulate_lifespan_gompertz 

# Step 1: Simulate lifespan
    lifespan = lifespan_model(start_age=start_age)
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

def monte_carlo(num_simulations=10000, lifespan_model=None):
    """
    Runs multiple simulations and estimates the probability of ruin.

    Returns:
        float: estimated probability of ruin.
    """
    ruin_count = 0
    for i in range(num_simulations):
        if run_simulation(lifespan_model=lifespan_model):
            ruin_count += 1
    return ruin_count / num_simulations

if __name__ == "__main__":
    prob_gompertz = monte_carlo(num_simulations=5000, lifespan_model = simulate_lifespan_gompertz)

    prob_normal = monte_carlo(num_simulations=5000, lifespan_model = simulate_lifespan)

    print(f"Gompertz Ruin Probability: {prob_gompertz:.2%}")
    print(f"Normal Ruin Probability: {prob_normal:.2%}")
