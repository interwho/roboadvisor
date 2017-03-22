from TradingAPI import TradingAPI

# Your desired portfolio contents and percentage ownership - The sum of all percentages should be no greater than 100
desired_portfolio = {
    "AAPL": 30.00,
    "IBM": 40.00,
    "STACKUP": 25.00,
    TradingAPI.CASH: 5.00
}

# What percentage are we allowed to be off? (To save trading commissions in the real world)
tolerance = 1.00

# How much cash should we start with?
cash_to_start = 10000

# Initialize the Trading API
trading_api = TradingAPI(cash_to_start)

# Convert the desired portfolio and tolerance into multipliers
for i in desired_portfolio:
    desired_portfolio[i] /= 100
tolerance /= 100

day_counter = 1
keep_trading = True
while keep_trading:
    print("--- DAY %s ---" % day_counter)

    # Get an updated portfolio
    portfolio = trading_api.get_portfolio()

    # Used to memoize prices so we don't need to make unnecessary API calls
    prices = dict()

    # Iterate over all stocks in our current portfolio
    total_value = 0
    for i in portfolio:
        # Calculate the total value of our portfolio (including cash)
        if i == TradingAPI.CASH:
            total_value += portfolio[i]
            continue
        price = trading_api.get_price(i)
        total_value += price * portfolio[i]
        print("%s costs $%s per share today" % (i, price))
        prices[i] = price

    # TODO: Build the rebalancing algorithm

    # Print a summary of our portfolio
    print("--- DAY %s RESULTS ---" % day_counter)
    print("Portfolio Starting Value: $%s" % cash_to_start)
    print("Portfolio Value: $%s" % round(total_value, 2))
    print("Portfolio Contents:")
    portfolio = trading_api.get_portfolio()
    for i in portfolio:
        if i == TradingAPI.CASH:
            print("CASH: $%s (%s percent of portfolio)" % (
                round(portfolio[i], 2), round((portfolio[i] / total_value) * 100, 2)))
        else:
            print("%s: %s shares (%s percent of portfolio)" % (
                i, round(portfolio[i], 2), round(((portfolio[i] * prices[i] * 100) / total_value), 2)))

    day_counter += 1
    keep_trading = not (input("Should we continue trading? (y/n)\n\n").lower() == 'n')
