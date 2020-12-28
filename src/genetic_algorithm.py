#!/usr/bin/env python
# coding: utf-8

# Genetic algorithm – This is the most popular type of EA (Evolutionary algorithm)

# In[1]:


import pandas as pd
import numpy as np
import random

from deap import base
from deap import creator
from deap import tools


# In[2]:


prot_cal_p_gram = 4
carb_cal_p_gram = 4
fat_cal_p_gram = 9

total_calories_per_day = 2500
total_calories_per_week = total_calories_per_day*7
percentage_prot = 0.3
percentage_carb = 0.5
percentage_fat = 0.2
