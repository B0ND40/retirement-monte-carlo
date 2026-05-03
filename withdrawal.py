def fixed_withdrawal(balance, withdrawal_amount):
    """
    Apply a fixed annual withdrawal to the portfolio.

    Parameters:
        balance (float): Current portfolio value
        withdrawal_amount (float): Annual withdrawal amount

    Returns:
        float: Updated portfolio balance (not allowed to go below zero)
    """

    new_balance = balance - withdrawal_amount

    # Prevent negative balances and return the updated balance.
    return max(new_balance, 0.0)