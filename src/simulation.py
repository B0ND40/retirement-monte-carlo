import numpy as np
import matplotlib.pyplot as plt

from src.portfolio import simulate_returns
from src.mortality import simulate_lifespan_normal, simulate_lifespan_gompertz
from src.withdrawal import fixed_withdrawal


def run_simulation(initial_balance=1_000_000, mu=0.05, sigma=0.15, withdrawal=80_000, 
                   start_age=65, lifespan_model=None):
    """
    Runs a single retirement simulation to determine if ruin occurs.
    Note: This function is a building block for the Monte Carlo function

    Parameters:
        initial_balance (float): Initial retirement portfolio balance (fixed at $1M in this case)
        mu (float): Expected annual return 
        sigma (float): Annual volatility (standard deviation of returns)
        withdrawal (float): Annual withdrawal amount 
        start_age (int): Retirement age 
        lifespan_model (callable, optional): Mortality model function

    Returns:
        bool: True if ruin occurs, False otherwise
    """

    # We simulate lifespan first to determine how many years we need to simualate returns & withdrawals.
    if lifespan_model is None:
        lifespan_model = simulate_lifespan_gompertz

    lifespan = lifespan_model(start_age=start_age)
    years = lifespan - start_age

    if years <= 0:
        return False

    returns = simulate_returns(mu, sigma, years)
    balance = initial_balance

    for annual_return in returns:
        balance *= annual_return
        balance = fixed_withdrawal(balance, withdrawal)

        if balance <= 0:
            return True # This implies ruin has occurred

    return False


def monte_carlo(num_simulations=10_000, initial_balance=1_000_000, mu=0.05, sigma=0.15, 
                withdrawal=80_000, start_age=65, lifespan_model=None):
    """
    Run multiple retirement simulations and estimate the probability of ruin.

    Parameters:
        num_simulations (int): Number of Monte Carlo trials
        initial_balance (float): Initial retirement portfolio balance
        mu (float): Expected annual return
        sigma (float): Annual volatility
        withdrawal (float): Annual withdrawal amount
        start_age (int): Retirement age
        lifespan_model (callable, optional): Mortality model function

    Returns:
        float: Estimated probability of ruin
    """
    ruin_count = 0

    # We use _ to indicate that we don't care about the loop variable
    for _ in range(num_simulations):
        if run_simulation(initial_balance=initial_balance, mu=mu, sigma=sigma, 
                          withdrawal=withdrawal, start_age=start_age, lifespan_model=lifespan_model):
            
            ruin_count += 1

    return ruin_count / num_simulations

def withdrawal_sensitivity(withdrawal_values, num_simulations=5_000, sigma=0.15, lifespan_model=None):
    """
    Compute ruin probabilities for a range of withdrawal amounts.

    Returns:
        list[tuple]: (withdrawal, ruin_probability)
    """
    results = []


    # We loop through each withdrawal amount and compute the corresponding ruin probability using the Monte Carlo function.
    for withdrawal in withdrawal_values:
        probability = monte_carlo(num_simulations=num_simulations, withdrawal=withdrawal,
                                  sigma=sigma, lifespan_model=lifespan_model)
        results.append((withdrawal, probability))

    return results


def sigma_sensitivity(sigma_values, num_simulations=5_000, lifespan_model=None):
    """
    Compute ruin probabilities for a range of volatility values.

    Returns:
        list[tuple]: (sigma, ruin_probability)
    """
    results = []

    for sigma in sigma_values:
        probability = monte_carlo(num_simulations=num_simulations,
                                  sigma=sigma, lifespan_model=lifespan_model)
        results.append((sigma, probability))

    return results


def plot_withdrawal_sensitivity_by_sigma(withdrawal_values, sigma_values, num_simulations=5_000):
    """
    Plot withdrawal sensitivity for multiple volatility levels
    under both Gompertz and Normal mortality models.
    """
    plt.figure(figsize=(10, 6))

    for sigma in sigma_values:
        gompertz_results = withdrawal_sensitivity(withdrawal_values, num_simulations=num_simulations,
                                                  sigma=sigma, lifespan_model=simulate_lifespan_gompertz)

        normal_results = withdrawal_sensitivity(withdrawal_values, num_simulations=num_simulations,
                                                sigma=sigma, lifespan_model=simulate_lifespan_normal)

        # Gompertz data
        withdrawals_g = []
        probs_g = []
        for w, p in gompertz_results:
            withdrawals_g.append(w)
            probs_g.append(p)

        # Normal data
        withdrawals_n = []
        probs_n = []
        for w, p in normal_results:
            withdrawals_n.append(w)
            probs_n.append(p)

        plt.plot(withdrawals_g, probs_g, marker="o", linestyle="-",
                 label=f"Gompertz, σ={sigma:.2f}")

        plt.plot(withdrawals_n,probs_n,marker="s",linestyle="--",
                 label=f"Normal, σ={sigma:.2f}")

    plt.xlabel("Yearly Withdrawal Amount")
    plt.ylabel("Ruin Probability")
    plt.title("Withdrawal Sensitivity for Different Volatility Levels")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_sigma_sensitivity(gompertz_results, normal_results):
    """
    Plot ruin probability vs volatility for both mortality models.
    """
    # Gompertz data
    sigmas_g = []
    probs_g = []

    for result in gompertz_results:
        s = result[0]      # First element is sigma
        p = result[1]      # Second element is probability
        sigmas_g.append(s)
        probs_g.append(p)

    # Normal data
    sigmas_n = []
    probs_n = []

    for result in normal_results:
        s = result[0]      # First element is sigma
        p = result[1]      # Second element is probability
        sigmas_n.append(s)
        probs_n.append(p)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(sigmas_g, probs_g, marker="o", label="Gompertz")
    plt.plot(sigmas_n, probs_n, marker="s", label="Normal")

    plt.xlabel("Volatility (Sigma)")
    plt.ylabel("Ruin Probability")
    plt.title("Ruin Probability vs Volatility")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_lifetime_distributions(num_simulations=10_000, start_age=65):
    """
    Plot Gompertz and Normal lifetime distributions.
    """
    normal_lifetimes = []

    for i in range(num_simulations):
        lifetime = simulate_lifespan_normal(start_age=start_age)
        normal_lifetimes.append(lifetime)


    gompertz_lifetimes = []

    for i in range(num_simulations):
        lifetime = simulate_lifespan_gompertz(start_age=start_age)
        gompertz_lifetimes.append(lifetime)

    # Optional diagnostic (to ensure we have some lifetimes at the max age)
    print("Normal P(T = 110):", np.mean(np.array(normal_lifetimes) == 110))
    print("Gompertz P(T = 110):", np.mean(np.array(gompertz_lifetimes) == 110))

    plt.figure(figsize=(10, 6))
    bins = range(start_age, 111, 2)

    plt.hist(normal_lifetimes, bins=bins, density=True, alpha=0.5, label="Normal")
    plt.hist(gompertz_lifetimes, bins=bins, density=True, alpha=0.5, label="Gompertz")

    plt.xlabel("Age at Death")
    plt.ylabel("Density")
    plt.title("Comparison of Lifetime Distributions")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_sample_path(
    initial_balance=1_000_000,
    mu=0.05,
    sigma=0.2,
    withdrawal=60_000,
    start_age=65,
    max_years=40
):
    balance = initial_balance
    balances = [balance]
    ruin_time = None

    returns = simulate_returns(mu, sigma, max_years)

    for r in returns:
        balance = balance * r
        balance = fixed_withdrawal(balance, withdrawal)
        balances.append(balance)

        if balance <= 0:
            ruin_time = len(balances) - 1
            break

    plt.figure()
    plt.plot(balances)
    plt.axhline(0, linestyle="--")

    if ruin_time is not None:
        plt.scatter(ruin_time, 0, s=80, zorder=5)
        plt.annotate(
            "Ruin",
            xy=(ruin_time, 0),
            xytext=(ruin_time - 4, max(balances) * 0.1),
            arrowprops=dict(arrowstyle="->")
        )

    plt.title("Example Portfolio Path")
    plt.xlabel("Years in Retirement")
    plt.ylabel("Portfolio Balance")
    plt.tight_layout()
    plt.show()


def compare_lifetime_models(num_simulations=10_000, start_age=65):
    """
    Print summary statistics comparing mortality models.
    """
    normal_lifetimes = []

    for i in range(num_simulations):
        lifetime = simulate_lifespan_normal(start_age=start_age)
        normal_lifetimes.append(lifetime)

    normal_lifetimes = np.array(normal_lifetimes)

    gompertz_lifetimes = []

    for i in range(num_simulations):
        lifetime = simulate_lifespan_gompertz(start_age=start_age)
        gompertz_lifetimes.append(lifetime)

    gompertz_lifetimes = np.array(gompertz_lifetimes)

    print("\n=== Lifetime Model Comparison ===\n")

    print(f"Normal mean: {np.mean(normal_lifetimes):.4f}")
    print(f"Gompertz mean: {np.mean(gompertz_lifetimes):.4f}\n")

    print(f"Normal P(T > 95): {np.mean(normal_lifetimes > 95):.4f}")
    print(f"Gompertz P(T > 95): {np.mean(gompertz_lifetimes > 95):.4f}")


def print_sensitivity_results(title, results, x_label):
    """
    Print sensitivity analysis results in a clean format.
    """
    print(f"\n{title}")

    for x_value, probability in results:
        if x_label == "$":
            print(f"${x_value:,.0f}: {probability:.2%}")
        else:
            print(f"{x_label}={x_value:.2f}: {probability:.2%}")


def run_analysis():
    """
    Run all analyses and plots.
    """
    withdrawals = [40_000, 50_000, 60_000, 70_000, 80_000, 90_000]
    sigma_values = [0.1, 0.2, 0.3, 0.4, 0.5]

    # Plot 1
    plot_withdrawal_sensitivity_by_sigma(
        withdrawals,
        sigma_values,
        num_simulations=5_000
    )

    # Plot 2
    gompertz_sigma_results = sigma_sensitivity(
        sigma_values,
        num_simulations=5_000,
        lifespan_model=simulate_lifespan_gompertz
    )

    normal_sigma_results = sigma_sensitivity(
        sigma_values,
        num_simulations=5_000,
        lifespan_model=simulate_lifespan_normal
    )

    plot_sigma_sensitivity(gompertz_sigma_results, normal_sigma_results)

    # Printed results
    gompertz_withdrawal_results = withdrawal_sensitivity(
        withdrawals,
        num_simulations=5_000,
        lifespan_model=simulate_lifespan_gompertz
    )

    normal_withdrawal_results = withdrawal_sensitivity(
        withdrawals,
        num_simulations=5_000,
        lifespan_model=simulate_lifespan_normal
    )

    print("\nWithdrawal Sensitivity at Default Sigma (0.15)")
    print_sensitivity_results("Gompertz Model", gompertz_withdrawal_results, "$")
    print_sensitivity_results("Normal Model", normal_withdrawal_results, "$")

    print_sensitivity_results(
        "Gompertz Volatility Sensitivity",
        gompertz_sigma_results,
        "Sigma"
    )
    print_sensitivity_results(
        "Normal Volatility Sensitivity",
        normal_sigma_results,
        "Sigma"
    )


if __name__ == "__main__":
    run_analysis()
    plot_lifetime_distributions(num_simulations=10_000)
    compare_lifetime_models(num_simulations=10_000)
    plot_sample_path()