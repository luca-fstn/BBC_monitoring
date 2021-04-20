#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 13:48:20 2021

@author: lucafaustini
"""

import time
import datetime


assets = {'Atlantia':'ATL.MI',     'Merck':'MRK'}
start  = {'Atlantia':'2020-03-08', 'Merck':'2021-02-18'}

conf = {'assets'    : assets,
        'start'     : start,
        'end'       : str(datetime.date.today()),
        'ff'        : True,
        'dd_win'    : 5
        }
    
tic     = time.time()

bt      = backtest(conf)
run     = bt.run()

tac     = time.time()
print('%s seconds'%(tac-tic))
print("finito")