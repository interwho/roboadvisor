from random import randrange


class TradingAPI:
    """A mock trading API"""

    CASH = "CASH"
    MAXIMUM_PERCENTAGE_CHANGE_PER_DAY = 4.00 * 1000
    MAXIMUM_INITIAL_STOCK_PRICE = 30.00 * 100

    def __init__(self, cash):
        self.portfolio = {
            self.CASH: round(cash, 2)
        }

        self.prices = dict()

    def get_portfolio(self):
        """Returns the portfolio dictionary"""
        return self.portfolio

    def get_price(self, ticker):
        """Returns the price of a ticker. Changes the price by a random percentage between -4 and 4 on each call."""
        if ticker == self.CASH:
            return False

        if ticker not in self.portfolio:
            self.portfolio[ticker] = 0

        if ticker in self.prices:
            self.prices[ticker] = round(self.prices[ticker] * (1 + (randrange(
                -1 * self.MAXIMUM_PERCENTAGE_CHANGE_PER_DAY, self.MAXIMUM_PERCENTAGE_CHANGE_PER_DAY, 1) / 100000)), 2)
            return self.prices[ticker]

        self.prices[ticker] = round((randrange(1, self.MAXIMUM_INITIAL_STOCK_PRICE) / 100), 2)
        return self.prices[ticker]

    def order(self, ticker, quantity):
        """Change the quantity of owned stock if there is enough cash"""
        if ticker == self.CASH:
            return False

        if ticker not in self.prices:
            # Generate a random price
            self.get_price(ticker)

        if quantity > 0:
            # Buy
            if self.portfolio[self.CASH] < (self.prices[ticker] * quantity):
                print("Not enough cash available to buy %s shares of %s!" % (quantity, ticker))
                return False
        else:
            # Sell
            if self.portfolio[ticker] < (-1 * quantity):
                print("You cannot sell more %s than you own!" % ticker)
                return False

        self.portfolio[ticker] += quantity
        self.portfolio[self.CASH] -= (self.prices[ticker] * quantity)
        return True
