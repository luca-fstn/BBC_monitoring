#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:10:34 2021

@author: lucafaustini

code with some function that we can use in our analysis, fell free to add more
"""
import pandas as pd
import numpy as np
import datetime


def load_ff(starting = datetime.datetime(2020,1,1)):
    """
    code that download fama french factor
    """
    import pandas_datareader as web
    
    # let us check the available datasets
    # sets = web.famafrench.get_available_datasets()


    # from the datasets let us download the FF factors and put them into one DataFrame
    startdt = starting

    d1 = web.DataReader('F-F_Research_Data_Factors_daily','famafrench',start=startdt)
    d2 = web.DataReader('F-F_Momentum_Factor_daily','famafrench',start=startdt)
    d3 = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily','famafrench',start=startdt)

    ff = d1[0]/100
    ff = ff.join(d2[0]/100, how = 'outer')
    ff5 = d3[0]/100
    ff = ff.join(ff5.loc[:,['RMW','CMA']], how = 'outer')

    ff.columns = [z.lower().strip() for z in ff.columns]
    ff.rename(columns = {'mkt-rf':'mktrf'}, inplace = True)

    ff = ff.loc[:,['mktrf', 'smb', 'hml', 'mom', 'rmw', 'cma','rf']]
    
    return ff
            

def ptf_perf(ptf, freq = 252, ddwin =0 ,period = ['1900','2100'], ff=0, tabs = True):
    
    # stats 
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from scipy import stats
    from scipy.optimize import minimize
    # table tools
    from astropy.table import Table 
    
    
    # compute portfolio returns
    ptf_val = ptf.copy()
    ptf_val = ptf_val[period[0]:period[1]]
    ret     = ptf_val.pct_change()
    
    # compute return-based performance 
    tot_ret     = ptf_val.iloc[-1]/ptf_val.iloc[0] - 1  #total return
    mean        = ret.mean()*freq             #annualized return
    std         = ret.std()*np.sqrt(freq)     #annualized vola
    sr          = mean/std
    
    
    mdd = 0
    if ddwin>1:
        mdd       = RMDD(ptf_val, ddwin).min()
    
    #fama french exposure
    alpha1f = 0
    alpha4f = 0
    if isinstance(ff, int):
        print('no factor given for alpha computation')
    else:
        retex = ret.sub(ff.rf,axis=0)
        retex.name = 'retex'
        retex = pd.concat([retex, ff.loc[:,['mktrf','smb','hml','mom']]], axis = 1)
        retex = retex.dropna()
        
        
        # run a regression using smf
        res = smf.ols(formula = 'retex~ mktrf', data = retex).fit()
        alpha1f = res.params[0]*freq
        res = smf.ols(formula = 'retex~ mktrf+smb+hml+mom', data = retex).fit()
        alpha4f = res.params[0]*freq
        
    
           
    
    data_rows = [('Total Return, %', round(100*tot_ret, 2)),
                 ('Mean, % p.a.', round(100*mean,2)),
                 ('Volatility, % p.a.', round(100*std,2)),
                 ('Sharpe Ratio, p.a.', round(sr,2)),
                 ('MDD, %  per period, ' + str(ddwin), round(mdd*100,2)),
                 ('1-factor alpha, % p.a.', round(100*alpha1f,2)),
                 ('4-factor alpha, % p.a.', round(100*alpha4f,2))
                 ]
    
    t = Table(rows=data_rows, names=(ptf.name, 'Full sample'), 
              meta={'name': 'perf table'},
              dtype=('S25', 'f8'))
    
    # print tables from inside the function
    if tabs: 
        print(t,'\n\n')
        #print(res.summary2())
    
    # return the required
    return [mean, std,sr,mdd, alpha1f, alpha4f],t
    

     # THE USE WOULD BE 


     # # # run the function to get the portfolio value process


     # # # run the function for portfolio performance     
     #stats, t = PtfPerf(ptf, freq = 252, ddwin = 30, period = ['2000','2019'], ff = ffd, tabs = True)


    
    

def RMDD(series, window_size, min_periods=1):
    """
    This code compute the rolling maximum drawdown for a pandas series.
    It first transform the series into an array, then split the array into mini array
    based on the window size and compute the maximum drawdown.
    It can be difficult to understand at first glance but is one of the most efficient way
    to compute the maxDD on python since avoids using the rolling function which is slow.
    """
    from numpy.lib.stride_tricks import as_strided
    
    ser = series.values #transform series into array
    
    def windowed_view(ser, window_size):
        """
        This function split the time series array in a sequence of sub-array with len
        equal to the window size. numpy.lib.stride_tricks is used to create the sub-arrays.
        
        Example:
            >>> ser = np.array([1,2,3,4,5,6])
            >>> windowed_view(ser, 3)
            array([[1,2,3],
                   [2,3,4],
                   [3,4,5],
                   [4,5,6]]).
        """
        
        y = as_strided(ser, shape=(ser.size-window_size +1, window_size),\
                       strides =(ser.strides[0], ser.strides[0]))
        return y
    
    """
    Compute the rolling maximum drawdown of 'ser'.
    'min_periods should satisfy '1 <= min_periods <= window_size'.
    Returns an 1d array with length 'len(ser) - min_periods + 1'.
    """
    
    if min_periods < window_size:
        pad = np.empty(window_size - min_periods)
        pad.fill(float(ser[0]))
        ser = np.append(pad, ser)
    
    y = windowed_view(ser, window_size)
    running_max_y = np.maximum.accumulate(y,axis=1)
    dd = y/running_max_y - 1
    dd = dd.min(axis=1)
    
    return pd.Series(dd, index = series.index)

            
            