#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 13:46:52 2021

@author: lucafaustini

this is the main filw where the backtest is compiled.
-run function run all the functions inside the class
-init get the inputs from the config.py file 
-load_data download with ffn the time series
-performance use the function in bbc_function to calculate various metrics

"""

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ffn
from pandas import ExcelWriter
import xlsxwriter
import openpyxl
import time
import os
import easychart

from config import Config
import bbc_function

class backtest:
    
    def run(self):
        self.load_data()
        self.performance()
        self.charts()
        return self
    
    def __init__(self, config_dict):
        #with config you allow the code to go to the file config.py and get inputs 
        self.config     = Config(config_dict)
        self.assets     = self.config.assets
        self.start      = self.config.start
        self.end        = self.config.end
        self.ff         = self.config.ff
        self.dd_win     = self.config.dd_win
        
        
    def load_data(self):
        
        self.ts = pd.concat([ffn.get(self.assets[ticker] +':Close',\
                                     start=self.start[ticker], \
                                     end = self.end)\
                             for ticker in self.assets.keys()], axis=1)
        self.ts.columns = self.assets.keys()

        
    
    def performance(self):
        
        self.perf = {}
        
        for ticker in self.assets.keys():
        
            if self.ff == True:
                famaf = bbc_function.load_ff()
            else:
                famaf = 0
            
            self.perf[ticker] = bbc_function.ptf_perf(ptf = self.ts[str(ticker)].dropna(),\
                                     freq = 252, ff = bbc_function.load_ff(),\
                                     ddwin = self.dd_win)
            
            
    def charts(self):
        
        """
        this is not working yet
        """
        
        chart       = easychart.new("column")
        chart.title = "Total Return Comparison"
        
        chart.categories       = self.ts.columns
        chart.yAxis.title.text = "Total Return in %"
        tot_ret = [self.ts[str(ticker)].dropna().iloc[-1] / \
                   self.ts[str(ticker)].dropna().iloc[0] - 1 \
                                  for ticker in self.assets.keys()]
        chart.plot(tot_ret, name=self.ts.columns)
        self.chart = chart
        

        self.data = {self.ts[str(ticker)].name : self.ts[str(ticker)].dropna() \
                        for ticker in self.assets.keys()}
        
        
        
            
        
       
        
        
            
            
        
            
        
            
        
        
            
            
        
    
            
    
