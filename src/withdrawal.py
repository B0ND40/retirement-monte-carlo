def fixed_withdrawal(balance, withdrawal_amount):
	"""
	Subtract a fixed withdrawal amount from the portfolio.

	Parameters:
		balance (float): current portfolio value
		withdrawal_amount (float): annual withdrawal

	Returns:
		float: updated balance
	"""
	return balance - withdrawal_amount

if __name__ == "__main__":
	print(fixed_withdrawal(100000, 40000)) # Fixed withdrawal example
