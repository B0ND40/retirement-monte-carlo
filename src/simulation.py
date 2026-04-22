from src.portfolio import simulate_returns
from src.mortality import simulate_lifespan, simulate_lifespan_gompertz
from src.withdrawal import fixed_withdrawal
import matplotlib.pyplot as plt


def run_simulation(initial_balance=1_000_000,mu=0.05,sigma=0.15,withdrawal=80_000,
                    start_age=65,lifespan_model=None):
    """
    Runs a single simulation of retirement portfolio sustainability.

    Returns:
        bool: True if ruin occurs, False otherwise.
    """
    if lifespan_model is None:
        lifespan_model = simulate_lifespan_gompertz

    lifespan = lifespan_model(start_age=start_age)
    years = lifespan - start_age

    if years <= 0:
        return False

    returns = simulate_returns(mu, sigma, years)
    balance = initial_balance

    for r in returns:
        balance *= r
        balance = fixed_withdrawal(balance, withdrawal)

        if balance <= 0:
            return True

    return False


def monte_carlo(num_simulations=10000, initial_balance=1_000_000,
                mu=0.05, sigma=0.15, withdrawal=80_000, start_age=65,
                  lifespan_model=None
                ):
    """
    Runs multiple simulations and estimates the probability of ruin.

    Returns:
        float: estimated probability of ruin.
    """
    ruin_count = 0

    # Counts how many simulations result in ruin and calculates the probability
    for i in range(num_simulations):
        if run_simulation(initial_balance=initial_balance, mu=mu, sigma=sigma,
                          withdrawal=withdrawal, start_age=start_age, 
                          lifespan_model=lifespan_model):
            ruin_count += 1
    return ruin_count / num_simulations

def compare_models(num_simulations=5000):
    """
    Compares the probability of ruin using Gompertz vs Normal lifespan models.

    Returns: None (prints results)
    """
    prob_gompertz = monte_carlo(
        num_simulations=num_simulations,
        lifespan_model=simulate_lifespan_gompertz
    )

    prob_normal = monte_carlo(
        num_simulations=num_simulations,
        lifespan_model=simulate_lifespan
    )

    print(f"Gompertz Ruin Probability: {prob_gompertz:.2%}")
    print(f"Normal Ruin Probability: {prob_normal:.2%}")

def withdrawal_sensitivity(withdrawal_values, num_simulations=5000, lifespan_model=None):
    """
    Analyzes how different withdrawal amounts affect the probability of ruin.

    Parameters:
        withdrawal_values (list): List of withdrawal amounts to test.
        num_simulations (int): Number of simulations to run for each withdrawal amount.

    Returns:
        list: List of tuples (withdrawal amount, ruin probability).
    """
    results = []

    # Loop through each withdrawal amount and calculate the ruin probability
    for w in withdrawal_values:
        prob = monte_carlo(num_simulations=num_simulations, withdrawal=w, 
                           lifespan_model=lifespan_model)
        results.append((w, prob))

    return results

def plot_withdrawal_sensitivity(gompertz_results, normal_results):
    """
    Plots the withdrawal sensitivity results for both Gompertz and Normal models.

    Parameters:
        gompertz_results (list): List of tuples (withdrawal amount, ruin probability) for Gompertz model.
        normal_results (list): List of tuples (withdrawal amount, ruin probability) for Normal model.
    """
    # Extract withdrawal amounts and probabilities for plotting
    withdrawals_g = [w for w, _ in gompertz_results]
    probs_g = [p for _, p in gompertz_results]

    withdrawals_n = [w for w, _ in normal_results]
    probs_n = [p for _, p in normal_results]

    plt.figure(figsize=(10, 6))
    plt.plot(withdrawals_g, probs_g, marker='o', label='Gompertz')
    plt.plot(withdrawals_n, probs_n, marker='s', label='Normal')
    plt.xlabel('Yearly Withdrawal Amount')
    plt.ylabel('Ruin Probability')
    plt.title('Withdrawal Sensitivity Analysis')
    plt.legend()
    plt.show()

if __name__ == "__main__":

    # Compare Gompertz vs Normal lifespan models
    withdrawals = [40_000, 50_000, 60_000, 70_000, 80_000, 90_000]

    gompertz_results = withdrawal_sensitivity(withdrawals, 
                            num_simulations=5000, 
                            lifespan_model=simulate_lifespan_gompertz)
    normal_results = withdrawal_sensitivity(withdrawals, 
                            num_simulations=5000,
                            lifespan_model=simulate_lifespan)
    plot_withdrawal_sensitivity(gompertz_results, normal_results)

    print("Gompertz Sensitivity:")
    for w, p in gompertz_results:
        print(f"${w:,.0f}: {p:.2%}")

    print("Normal Sensitivity:")
    for w, p in normal_results:
        print(f"${w:,.0f}: {p:.2%}")