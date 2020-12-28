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

cal_prot = round(percentage_prot * total_calories_per_week)
cal_carb = round(percentage_carb * total_calories_per_week)
cal_fat = round(percentage_fat * total_calories_per_week)


# In[3]:


#goal grams
gram_prot = cal_prot / prot_cal_p_gram
gram_carb = cal_carb / carb_cal_p_gram
gram_fat = cal_fat / fat_cal_p_gram


# In[4]:


products = pd.read_csv("food.csv")


# In[5]:


products


# In[6]:


cal_data = products[['Gram_Prot', 'Gram_Fat', 'Gram_Carb']]

prot_data = list(cal_data['Gram_Prot'])
fat_data = list(cal_data['Gram_Fat'])
carb_data = list(cal_data['Gram_Carb'])

