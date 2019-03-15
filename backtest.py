import numpy as np
import pandas as pd

def sharpe_ratio(x):
    return  16 * x.mean() / x.std()


def run_backtest(price_data, indicator, lookback=20, buy_constant=0.0, sell_constant=0.0, start_date='2001-01-01', years=None,
                unit_move=35.0, transaction_cost=90.96):
    
    open_prices = price_data.Open
    close_prices = price_data.Close
    
    indicator_values = close_prices.rolling(window=lookback).apply(indicator, raw=True)
    
    if years == None: # create a list of all the years for the backtest
        years = list(indicator_values[start_date:].index.year.unique())    
    
    trade_directions = pd.Series(0.0, index=indicator_values.index)
    trade_directions[indicator_values > buy_constant] = 1.0    # Long
    trade_directions[indicator_values < sell_constant] = -1.0  # Short

    # calculate the eod positions and the order quantities for each day
    eod_position = trade_directions.shift(1)
    order_quantity = eod_position - eod_position.shift(1)
    order_quantity[start_date:][0] = eod_position[start_date:][0]
    
    # calculate the daily pnl of the strategy
    current_position_pnl = eod_position.shift(1) * (close_prices - close_prices.shift(1)) * unit_move
    current_position_pnl[start_date:][0] = 0.0
    new_trade_pnl = order_quantity * (close_prices - open_prices) * unit_move
    transaction_costs = -transaction_cost * order_quantity.abs() 
    daily_pnl = current_position_pnl + new_trade_pnl + transaction_costs
    
    mask = daily_pnl.index.year.isin(years) & (daily_pnl.index >= start_date)
    
    daily_pnl = daily_pnl[mask]
    
    # calculate the Sharpe ratios 
    sharpe_ratios_raw = [sharpe_ratio(daily_pnl[str(year)]) for year in years]
    sharpe_ratios = pd.DataFrame(sharpe_ratios_raw, index=years, columns=['Sharpe Ratio']).round(4)
    average_sharpe_ratio = np.mean(sharpe_ratios_raw).round(2) 

    return daily_pnl, average_sharpe_ratio, sharpe_ratios