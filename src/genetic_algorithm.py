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


# In[7]:


def purchases():
    return random.choices( range(0, 22), k = len(products))


# In[8]:


def cost(person):
    person = person[0]
    tot_prot = sum(x*y for x,y in zip(prot_data,person))
    tot_fat = sum(x*y for x,y in zip(fat_data,person))
    tot_carb = sum(x*y for x,y in zip(carb_data,person))
    u = prot_cal_p_gram * tot_prot + carb_cal_p_gram * tot_carb + fat_cal_p_gram * tot_fat
    
    return abs(u - total_calories_per_week), abs(tot_prot - gram_prot), abs(tot_fat - gram_fat), abs(tot_carb - gram_carb),


# In[9]:


weights = (-1, -1/0.3, -5, -2)
creator.create("FitnessMin", base.Fitness, weights=weights)
creator.create("Person", list, fitness=creator.FitnessMin)


# In[10]:


toolbox = base.Toolbox()


# In[11]:


toolbox.register("purchases", purchases)
toolbox.register("person", tools.initRepeat, creator.Person, toolbox.purchases, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.person)

toolbox.register("cost", cost)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("cost", cost)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


pop = toolbox.population(n=100)


# In[14]:


fitnesses = list(map(toolbox.cost, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit


# In[15]:


# CXPB вероятность скрещивания
# MUTPB вероятность мутации
CXPB, MUTPB = 0.3, 0.5


# In[16]:


fits = [ind.fitness.values[0] for ind in pop]


# In[17]:


generation = 0
while generation < 5000:
    generation+=1
    if generation < 10 or generation > 4890:
        print("-- Поколение %i --" % generation)
    
    offspring = toolbox.select(pop, len(pop))
    offspring = list(map(toolbox.clone, offspring))
    
    # Скрещивание
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1[0], child2[0])
            del child1.fitness.values
            del child2.fitness.values
            
    # Мутирование
    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant[0])
            del mutant.fitness.values
            
    # Оценивание
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.cost, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    pop[:] = offspring
    
    # Отбор
    fits = [ind.fitness.values[0] for ind in pop]
    
    length = len(pop)
    mean = sum(fits) / length
    _sum = sum(x*x for x in fits)
    std = abs(_sum / length - mean**2)**0.5
    
    if generation < 10 or generation > 4890:
        print(min(fits), max(fits), mean, std)
    elif generation == 10:
        print("...")


# In[18]:


best = pop[np.argmin([toolbox.cost(x) for x in pop])]


# In[19]:


products['multivariate_choice'] = pd.Series(best[0])

products['multivariate_gram_prot'] = products['multivariate_choice'] * products['Gram_Prot']
products['multivariate_gram_fat'] = products['multivariate_choice'] * products['Gram_Fat']
products['multivariate_gram_carb'] = products['multivariate_choice'] * products['Gram_Carb']
products['multivariate_cal'] = products['multivariate_choice'] * products['Calories']


# In[20]:


products[['Name', 'multivariate_choice', 'multivariate_cal']]