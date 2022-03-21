import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import numpy as np
import pandas as pd
import datetime
from datetime import datetime
from dbConnection import getDBURL
from sqlalchemy import create_engine

def anchorScrape():
	date = datetime.now().strftime('%Y-%m-%d')


	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
	driver.get("https://app.anchorprotocol.com/")
	#the element is not loading immediately, it loads immediately with value 0, so sleep 5 sec
	time.sleep(20)
	#I think the webdriverwait could be removed here, but its probably best to fix it and remove the sleep
	try:
		#scrape reserves from anchor
		element = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[1]/div/main/div/div[2]/section[1]/div/section[2]/p/span[1]/span"))
		)
		reserves = element.text 
		reserves = int(reserves.replace(',', ''))
		print(reserves)
	finally:
		driver.quit()

	#select statement to get previous observations
	url = getDBURL()
	my_conn=create_engine(url)   
	sql = "SELECT * FROM `anchor_reserves`"
	data = pd.read_sql(sql, my_conn)
	#input the newest observation at the last row in the dataframe
	data.loc[len(data.index)] = [date, reserves, 0]

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

	###write reserves and prediction to db
	newRow = {'date' : [date], 'reserves' : [reserves], 'timeline': [daysRemaining]}
	df = pd.DataFrame(newRow, columns = ['date', 'reserves', 'timeline'])
	df.to_sql('anchor_reserves', my_conn, if_exists='append', index = False)
