#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 13:47:08 2021

@author: lucafaustini
"""
class Config:
    def __init__(self, config):
        self.assets      = config.get('assets')
        self.start       = config.get('start')
        self.end         = config.get('end')
        self.ff          = config.get('ff')
        self.dd_win      = config.get('dd_win')
