import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from csv import writer
from selenium import webdriver
import numpy as np
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get("https://app.anchorprotocol.com/")
#the element is not loading immediately, it loads immediately with value 0, so sleep 5 sec
time.sleep(5)
#I think the webdriverwait could be removed here, but its probably best to fix it and remove the sleep
try:
	#scrape reserves from anchor
	element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[1]/div/main/div/div[2]/section[1]/div/section[2]/p/span[1]/span"))
    )
	reserves = element.text 
	reserves = int(reserves.replace(',', ''))
	print(reserves)
finally:
	driver.quit()


#add row to df with new reserves obsersation
data = pd.read_csv('C:\\Users\\Chase\\Documents\\datasets\\anchorReserves.csv')
data.loc[len(data.index)] = [datetime.now(), reserves, 0]


#least squares regression
X = data.index
Y = data['reserves'].values

mean_x = np.mean(X)
mean_y = np.mean(Y)

n = len(X)

numer = 0
denom = 0
for i in range(n):
	numer += (X[i] - mean_x) * (Y[i] - mean_y)
	denom += (X[i] - mean_x) ** 2
m = numer / denom
c = mean_y - (m * mean_x)

#calculate days remaining based on lsr slope 
daysRemaining = c/abs(m)

#write reserves and prediction to db
df = pd.DataFrame([[datetime.now(), reserves, daysRemaining]])
df.to_csv('C:\\Users\\Chase\\Documents\\datasets\\anchorReserves.csv', mode='a', index=False, header=False)