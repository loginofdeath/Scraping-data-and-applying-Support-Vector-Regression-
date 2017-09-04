from selenium import webdriver
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, re, json, numpy as np
import pickle
import pandas as pd

distributor, totalgross, marketshare, moviestracked, moviestrackedCurrent = ([] for i in range(5))
browser = webdriver.Chrome()

url_form = "http://www.boxofficemojo.com/studio/?view=company&view2=yearly&yr={}&p=.htm"
distributor_list=[]
totalgross_list=[]
marketshare_list=[]
moviestracked_list=[]
moviestrackedCurrent_list=[]

for i in range(2000,2018):
    url = url_form.format(i)
    browser.get(url)
    distributor = browser.find_elements_by_xpath("//div[contains(@id, 'body')]//tbody//tbody//a//b")
    distributor=list(map(lambda x: x.text, distributor))
    distributor_list.append(distributor)
    totalgross = browser.find_elements_by_xpath("//*[@id='body']/table[3]/tbody/tr/td/table/tbody/tr/td[4]/font")
    totalgross=list(map(lambda x: x.text, totalgross))
    totalgross_list.append(totalgross)
    marketshare = browser.find_elements_by_xpath("//*[@id='body']/table[3]/tbody/tr/td[1]/table/tbody/tr/td[3]/font/b")
    marketshare=list(map(lambda x: x.text, marketshare))
    marketshare_list.append(marketshare)
    moviestracked = browser.find_elements_by_xpath("//*[@id='body']/table[3]/tbody/tr/td[1]/table/tbody/tr/td[5]/font")
    moviestracked=list(map(lambda x: x.text, moviestracked))
    moviestracked_list.append(moviestracked)
    moviestrackedCurrent = browser.find_elements_by_xpath("//*[@id='body']/table[3]/tbody/tr/td[1]/table/tbody/tr/td[6]/font")
    moviestrackedCurrent=list(map(lambda x: x.text, moviestrackedCurrent))
    moviestrackedCurrent_list.append(moviestrackedCurrent)

with open('distributor_list.pkl', 'wb') as f:
    pickle.dump(distributor_list, f)
with open('totalgross_list.pkl', 'wb') as f:
    pickle.dump(totalgross_list, f)
with open('marketshare_list.pkl', 'wb') as f:
    pickle.dump(marketshare_list, f)
with open('moviestracked_list.pkl', 'wb') as f:
    pickle.dump(moviestracked_list, f)
with open('moviestrackedCurrent_list.pkl', 'wb') as f:
    pickle.dump(moviestrackedCurrent_list, f)

df=pd.DataFrame({
    'Year':[],
    'Distributor':[],
    'Total_Gross':[],
    'No_of_movies':[]
})
with open('distributor_list.pkl', 'rb') as f:
    distributor_list = pickle.load(f)
with open('moviestracked_list.pkl', 'rb') as f:
    moviestracked_list = pickle.load(f)
with open('moviestrackedCurrent_list.pkl', 'rb') as f:
    moviestrackedCurrent_list = pickle.load(f)
with open('totalgross_list.pkl', 'rb') as f:
    totalgross_list = pickle.load(f)
for i in range(0,18):
    totalgross_list[i].pop(0)
for i in range(0,18):
    for j in range(len(totalgross_list[i])):
         totalgross_list[i][j]=''.join(totalgross_list[i][j][1:].split(','))
for i in range(0,18):
    for j in range(len(totalgross_list[i])):
        if 'k' in totalgross_list[i][j]:
            totalgross_list[i][j]=float(totalgross_list[i][j].split('k')[0])/1000
with open('totalgross_list_mod.pkl', 'wb') as f:
    pickle.dump(totalgross_list, f)
for i in range(0,18):
    marketshare_list[i].pop(0)
for i in range(0,18):
    for j in range(len(marketshare_list[i])):
         marketshare_list[i][j]=float(marketshare_list[i][j].split('%')[0])
for i in range(0,18):
    moviestrackedCurrent_list[i].pop(0)
with open('marketshare_list_mod.pkl', 'wb') as f:
    pickle.dump(marketshare_list, f)
for i in range(18):
    temp_df=pd.DataFrame({
    'Year':[yr+i]*len(distributor_list[i]),
    'Distributor':distributor_list[i],
    'Total_Gross':totalgross_list[i],
    'No_of_movies':moviestrackedCurrent_list[i]
        
})
    
    df=df.append(temp_df)
with open('dataframe.pkl', 'wb') as f:
    pickle.dump(df, f)

df.to_csv('box_office_luther.csv')

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
sc_y = StandardScaler()
X = sc_X.fit_transform(X)
y = sc_y.fit_transform(y)

from sklearn.svm import SVR
regressor = SVR(kernel = 'rbf')
regressor.fit(X, y)

y_pred = regressor.predict(2018)
print(sc_y.inverse_transform(y_pred))


