def initialize(context):
    
    # The initialize function sets any data or variables that you'll use in your algorithm. 
    # For instance, you'll want to define the security (or securities) you want to backtest.  
    # You'll also want to define any parameters or values you're going to use later. 
    # It's only called once at the beginning of your algorithm.
    
    # In our example, we're looking at Apple.  If you re-type this line 
    # yourself, you'll see the auto-complete that is available for security. 

    context.security = symbol('AAPL')

# The handle_data function is where the real work is done.  
# This function is run either every minute (in live trading and minutely backtesting mode) 
# or every day (in daily backtesting mode).
def handle_data(context, data):
    
    
    # We've built a handful of useful data transforms for you to use.  In this 
    # line, we're computing the volume-weighted-average-price of the security 
    # defined above, in the context.security variable.  
    
    # To make market decisions, we will need to know the stock's average price for the last 5 days,
    # and the stock's current price. 
    average_price = data[context.security].mavg(5)
    current_price = data[context.security].price
    price_stddev  = data[context.security].stddev(5)
    if price_stddev == None:
        price_band = current_price/10
    else:
        price_band = 1.75 * price_stddev
    
    # Another powerful built-in feature of the Quantopian backtester is the
    # portfolio object.  The portfolio object tracks your positions, cash,
    # cost basis of specific holdings, and more.  In this line, we calculate
    # the current amount of cash in our portfolio.   
    cash = context.portfolio.cash
    
    # Here is the meat of our algorithm.
    # If the current price is 1% above the 5-day average price AND we have enough cash, then we will order.
    # If the current price is below the average price, then we want to close our position to 0 shares.
    if current_price < 1.01*average_price - price_band:
        
        # Need to calculate how many shares we can buy
        number_of_shares = int(cash/current_price)
        
        # Place the buy order (positive means buy, negative means sell)
        order(context.security, + 2* number_of_shares)
        log.info("Buying %s" % (context.security.symbol))
        

    elif current_price > 1.01*average_price + price_band:
        
        # Sell all of our shares by setting the target position to zero
        number_of_shares = int(cash/current_price)
        order(context.security, - 0.5* number_of_shares)
        log.info("Selling %s" % (context.security.symbol))
    
    # You can use the record() method to track any custom signal. The record graph
    # will track up to five different variables. Here we record the Apple stock price.
    record(stock_price=data[context.security].price)