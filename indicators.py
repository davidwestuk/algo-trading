def PFE(prices):
    """Polarised Fractal Efficiency (PFE)"""
    # prices[-1] is the latest price in our rolling window
    # prices[0] is the oldest price in our rolling window
    
    count = len(prices)
    top = ((prices[-1] - prices[0])**2 + (count - 1)**2)**0.5
    
    bottom = 0.0
    for i in range(count - 1):
        bottom += ((prices[i+1] - prices[i])**2 + 1)**0.5 
        
    if prices[-1] < prices[0]:
        top = -top
        
    return top / bottom
