from selenium import webdriver
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains
import time
import configparser
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

sportBet_accounts = []
accounts = UserAccount.objects.all().values_list('email', 'username', 'password', 'website')
accounts_list = list(accounts)
accounts = [{'email': tup[0], 'username': tup[1], 'password': tup[2], 'betting_site': tup[3]} for tup in
			accounts_list]
print(accounts)
for i in accounts:
	if i["betting_site"] == "Sportybet":
		sportBet_accounts.append(i)
options = Options()
options.add_argument('--disable-gpu')
# options.add_argument('--headless')
browser = webdriver.Chrome()



xPathLogin = '//*[contains(concat( " ", @class, " " ), concat( " ", "font-weight-black", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "v-btn__content", " " ))]'
xPathEmail =  './/input[@placeholder="Mobile Number"]'
xPathPassword = './/input[@placeholder="Password"]'
xPathSubmitLogin = '//*[contains(concat( " ", @class, " " ), concat( " ", "font-weight-black", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "v-btn__content", " " ))]'

#1xbet login successful confirmation xpath
xPathMyAccount = '//*[@id="app"]/div/div[1]/header/div[1]/div[3]/div/button[2]/span'


def placebet(url, bet_columns, username, password):
	browser.get(url)
	time.sleep(1)
	try:
		time.sleep(1)
		usernameEl = browser.find_element(By.XPATH,xPathEmail)
		passwordEl = browser.find_element(By.XPATH,xPathPassword)
		usernameEl.send_keys(username)
		time.sleep(1)
		passwordEl.send_keys(password)
		time.sleep(1)
		browser.find_element(By.XPATH,xPathSubmitLogin).click()
		WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, xPathMyAccount)))
	except:
		pass


	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	time.sleep(4)
	correct_score=browser.find_element(By.XPATH,"//*[text()='Correct Score ']")
	correct_score.click()
	# time.sleep(200)
	print('correct score dropdown click')
	time.sleep(3)

	bets=browser.find_elements(By.XPATH,".//div[@data-test-id='market-body-base-component']")
	# Read values from the CSV file and store them in a list


	
	for bet in bets:
		if bet.text == bet_columns:
			print(f' Bet Column: {bet_columns}, Bet: {bet.text}')
			bet.click()
	print(bet_columns)
	
	# input count4
	# time.sleep(400)
	# Scroll to the top of the page using JavaScript
def execute_bet():
	browser.execute_script("window.scrollTo(0, 0);")
	count=browser.find_element(By.XPATH,'.//input[@class="text-right input text-body-1"]')
	count.click()
	count.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
	count.send_keys(Keys.BACKSPACE) 
	count.send_keys('0.5')
	time.sleep(5)
	#click confirm bet
	place=browser.find_element(By.XPATH,'//*[@id="betNowBtn"]')
	place.click()
	print('place bet click')
	time.sleep(7)
	
	

	
	ok=browser.find_elements(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "primary", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "v-btn__content", " " ))]')[-1]
	ok.click()
	time.sleep(4)

def cashout_func():
	# #click mybet 
	mybet=browser.find_element(By.XPATH,"//*[@id='app']/div/div[1]/header/div[2]/div/div/div[2]/div/button[2]")
	mybet.click()
	time.sleep(5)


	cashout_count=browser.find_elements(By.XPATH,'//*[@id="2"]/div/div/div[2]/div/div/div/div/div[1]/div[3]/span/div/div[1]/div[2]/button[1]')
	print('cashout_count :',len(cashout_count))
	if len(cashout_count) >=1:
		for i in range(0,len(cashout_count)):
			try:
				browser.find_elements(By.XPATH,'')[i].click()
			except:
				browser.find_element(By.XPATH,'//*[@id="2"]/div/div/div[2]/div/div/div/div/div[1]/div[3]/span/div/div[1]/div[2]/button[1]').click()
			time.sleep(3)
			
			
			cashout_confirm= browser.find_element(By.XPATH,'//*[@id="0"]/div/div[2]/button[2]/span/span')
			cashout_confirm.click()
			time.sleep(3)
			try:
				close=browser.find_element(By.XPATH,'//*[@id="app"]/div[4]/main/div[2]/div/div/div/div[2]/button')
				close.click()
				
			except:
				pass
				
			
			time.sleep(3)
			
			print(f'Cashout done {i}')



def execute():
	# Replace 'username' and 'password' with actual values
	csv_file_path = uploaded_file
	results = []
	df = pd.read_csv(csv_file_path, header=None)
	total_rows, total_columns = df.shape
	print(uploaded_file)
	print(total_rows)
	print(total_columns)
	all_results = []

	print('sportBet_accounts',sportBet_accounts)
	random_accounts = (sportBet_accounts)
	print(len(random_accounts))
	for i in range(0,len(random_accounts)):
		username = random_accounts[i]["username"]
		password =random_accounts[i]["password"]
	# # Replace 'username' and 'password' with actual values
	# username = '0598029696'
	# password = 'NVW6kfc4eax_wnc9etm'

			

		try:
		# Remove empty strings and single quotes
			urls_list = [item.strip("'") for item in urls if item]
		# Iterate through columns
			for i in range(len(df.columns)):
				# Iterate through URLs
				for j, url in enumerate(urls_list):
					# Use the value from the corresponding column and row
					bet = df.iloc[j, i]

					# Call the placebet function
					print(f'URL: {url}, Column: {i + 1}, Row: {j + 1}, Bet: {bet}')
					try:
						placebet(url, bet, username, password)
					except:
						print('match over')
						pass

			

					time.sleep(2)

				# Execute the betslip function after completing all URLs for a column
				execute_bet()

			
			# cashout_func()
		except Exception as e:
			print(e)
if __name__ == "__main__":
	execute()
