#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 22:13:26 2017

@author: bob
"""
import os
import pandas as pd
#from xml.etree import ElementTree
import numpy as np
#from numpy import nan
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import datetime as dt
#import matplotlib.dates as mdates


# load file to pandas df 
file_name = 'vysledky.csv' 
#base_path = os.path.dirname(os.path.realpath('__file__'))
base_path = "/home/bob/Documents/python_projects/silesia/"
file = os.path.join(base_path, file_name)
df = pd.read_csv(file, sep=',', header=0, 
                 usecols=['Kat','Ročník', 'M/Z','Cíl'],
                 engine='python')

df['Delta'] = pd.to_datetime(df['Cíl'])-pd.to_datetime('today') # čas konverze
bins = np.histogram(df["Ročník"], bins=5)       # rozdělí ročníky do 5ti intervalů
#bins = np.histogram(df["Ročník"], bins='auto') # intervaly automaticky
cat = pd.cut(df["Ročník"], bins[1])             # zařadí ročníky do kategorií
df['cat'] = cat                                 # přiřadit kategorie do df

#sns.boxplot(x=pd.Categorical(df['Ročník']), y=df["Delta"].astype('timedelta64[m]'), hue = df['M/Z'], data=df)
plt.xticks(rotation=90)                         # otočit popis stupnice osy y
sns.boxplot(x=df['cat'], y=df["Delta"].astype('timedelta64[m]'), hue = df['M/Z'], data=df, palette="Set2")
sns.plt.show()     



sns.violinplot(x=df['cat'], y=df["Delta"].astype('timedelta64[m]'), hue = df['M/Z'], data=df, split=True, palette="Set2")
sns.plt.show()     
                           # boxplots dle kategorií, čas v minutách, rozdělit M/Z

# spočítat průměr pro každou kategorii
print df['Delta'].astype('timedelta64[m]').groupby(df['cat']).mean()
# spočítá median pro kategorie rozdělené na M/Z
print df['Delta'].astype('timedelta64[m]').groupby([df['cat'], df['M/Z']]).median()
# rozdělit do dvou sloupců .unstack()
print df['Delta'].astype('timedelta64[m]').groupby([df['cat'], df['M/Z']]).median().unstack()
# nebo tato syntaxe 
print df.groupby(['cat', 'M/Z'])[['Ročník']].mean().unstack()