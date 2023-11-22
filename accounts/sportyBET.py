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


options = Options()
options.add_argument('--disable-gpu')
# options.add_argument('--headless')
browser = webdriver.Chrome()

# 1xbet login xpaths
xPathLogin = '//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/button'
xPathEmail = '//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/input'
xPathPassword = '//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/input'
xPathSubmitLogin = '//*[@id="j_page_header"]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/button'
# 1xbet login successful confirmation xpath
xPathMyAccount = '//*[@id="j_userInfo"]/span'

def placebet(url, bet_columns, username, password):
    browser.get(url)
    time.sleep(1)
    try:
        browser.find_element(By.XPATH, xPathLogin).click()
        time.sleep(3)

        usernameEl = browser.find_element(By.XPATH, xPathEmail)
        passwordEl = browser.find_element(By.XPATH, xPathPassword)
        usernameEl.send_keys(username)
        time.sleep(1)
        passwordEl.send_keys(password)
        time.sleep(1)
        browser.find_element(By.XPATH, xPathSubmitLogin).click()
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, xPathMyAccount)))
        time.sleep(2)


    except :
        pass

    correct_score = browser.find_element(By.XPATH, "//*[text()='Correct Score']")
    correct_score.click()
    table = browser.find_element(By.XPATH,
                                    "//span[text()='Correct Score']/ancestor::div[1]/ancestor::div[1]/ancestor::div[1]/following-sibling::div")

    # for bet_column in bet_columns:
        # search_values = []
        # with open('output.csv', 'r') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         search_values.append(row[bet_column])

    bets = table.find_elements(By.XPATH, ".//span[@class='m-table-cell-item']")
    for bet in bets:
        if bet.text == bet_columns:
            print(f' Bet Column: {bet_columns}, Bet: {bet.text}')
            bet.click()
    print(bet_columns)
def execute_bet():
    time.sleep(4)
    browser.execute_script("window.scrollTo(0, 0);")
    count = browser.find_element(By.XPATH, './/span[@class="m-input-com"]/input')
    count.click()
    count.send_keys(Keys.CONTROL + "a")
    count.send_keys(Keys.BACKSPACE)
    count.send_keys('0.1')
    time.sleep(2)
    place = browser.find_element(By.XPATH, '//*[@id="j_betslip"]//button')
    place.click()
    print('place bet click')
    time.sleep(7)
    place.click()
    confirm = browser.find_element(By.XPATH, "//*[text()='Confirm']")
    confirm.click()
    time.sleep(3)
    ok = browser.find_element(By.XPATH, "//*[text()='OK']")
    ok.click()
    time.sleep(1)
    
def cashout_func():
    cashout_count = browser.find_element(By.XPATH,
                                        '//*[@id="j_betslip"]/div[1]/div[1]/div[3]/div/span[2]').text
    print('cashout_count:', cashout_count)
    if int(cashout_count) >= 1:
        for i in range(0, int(cashout_count)):
            time.sleep(3)
            cashout_button = browser.find_element(By.XPATH, '//*[@id="j_betslip"]/div[1]/div[1]/div[3]')
            cashout_button.click()
            time.sleep(3)
            cashout = browser.find_element(By.XPATH,
                                        '//*[@id="j_betslip"]/div[3]/ul/li/div[2]/div[4]/div[2]/div[5]/button')
            cashout.click()
            time.sleep(1)
            cashout_confirm = browser.find_element(By.XPATH,
                                                '//*[@id="j_betslip"]/div[3]/ul/li/div[2]/div[4]/div[2]/div[1]/div[2]/button[2]/span/span')
            cashout_confirm.click()
            time.sleep(3)
            print(f'Cashout done {i}')





import pandas as pd
import time

def execute():
    # Replace 'username' and 'password' with actual values
    username = '0598029696'
    password = 'NVW6kfc4eax_wnc9etm'

    csv_file_path = 'bets.csv'
    urls = [
        'https://www.sportybet.com/gh/sport/football/England/Premier_League/Man_City_vs_Liverpool/sr:match:41763091',
        'https://www.sportybet.com/gh/sport/football/England/Premier_League/Burnley_vs_West_Ham/sr:match:41763083',
        'https://www.sportybet.com/gh/sport/football/England/Premier_League/Luton_vs_Crystal_Palace/sr:match:41763089'
    ]

    try:
        # Read the CSV file and get the list of bets
        df = pd.read_csv(csv_file_path, header=None)

       # Iterate through columns
        for i in range(len(df.columns)):
            # Iterate through URLs
            for j, url in enumerate(urls):
                # Use the value from the corresponding column and row
                bet = df.iloc[j, i]

                # Call the placebet function
                print(f'URL: {url}, Column: {i + 1}, Row: {j + 1}, Bet: {bet}')
                try:
                    placebet(url, bet, username, password)
                except:
                    print('match over')
                    pass

        

                time.sleep(5)

            # Execute the betslip function after completing all URLs for a column
            execute_bet()

        
        cashout_func()
    except Exception as e:
        print(e)
if __name__ == "__main__":
    execute()
