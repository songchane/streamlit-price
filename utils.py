# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 16:29:09 2024

@author: lcsdc
"""

API_KEY = '6a6f6c57776a6961353445704a6c6b'

import pandas as pd

def load_data():
    data = pd.read_csv('price2.csv')
    return data
