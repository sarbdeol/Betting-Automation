import io
import random

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from selenium.webdriver import Keys
from .models import UserAccount
from .forms import UserAccountForm
import logging
import csv
import time
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

logger = logging.getLogger('my_logger')


def index(request):
    accounts = UserAccount.objects.all()
    form = UserAccountForm()
    context = {'accounts': accounts, 'form': form}
    return render(request, 'accounts/index.html', context)


def add_account(request):
    try:
        if request.method == 'POST':
            form = UserAccountForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    print(f"Error saving data: {e}")
        else:
            return redirect('index')
    except Exception as e:
        print(e)
    return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def execute(request):
    return render(request, 'accounts/execute.html')


@csrf_exempt
def upload_excel(request):
    if request.method == 'POST':
        # Get the selected bots and URLs from the POST data
        selected_bot = request.POST.get('selected_bots')
        # print('selected_bot:',selected_bot)
        urls = [request.POST.get(f'urlBot{selected_bot}{i}') for i in range(1, 8)]
        # print(urls)
        # Get the uploaded file
        uploaded_file = request.FILES['excelFile']
        # print(uploaded_file)
        response_data = {
            'selected_bot': selected_bot,
            'URLS': urls,
            'csv_path': f"{uploaded_file}"  # Assuming your file field is in models and has an `upload_to` parameter
        }
        print(response_data)
        

        if selected_bot == "A":
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
                    usernameEl.clear()
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

            def logout():
                logout = browser.find_element(By.XPATH, '//*[@id="j_userInfo"]/span')
                logout.click()
                time.sleep(1)
                logout_btn = browser.find_element(By.XPATH, '//*[@id="j_userInfo"]/ul/li[8]')
                logout_btn.click()
                print('log out')
                time.sleep(3)
            def execute_bet():
                print('execute_bet')
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

            def execute():
                csv_file_path = uploaded_file
                results = []
                df = pd.read_csv(csv_file_path, header=None)
                total_rows, total_columns = df.shape
                print(uploaded_file)
                print(total_rows)
                print(total_columns)
                all_results = []

                print('sportBet_accounts',len(sportBet_accounts))
               # Assuming you have 2 accounts
                num_accounts = len(sportBet_accounts)
                columns_per_account = df.shape[1] // num_accounts

                # Iterate through each account
                for account_index, account in enumerate(sportBet_accounts):
                    username = account["username"]
                    password = account["password"]

                    try:
                        # Remove empty strings and single quotes
                        urls_list = [item.strip("'") for item in urls if item]
                        
                        # Determine the range of columns for the current account
                        start_col = account_index * columns_per_account
                        end_col = (account_index + 1) * columns_per_account

                        # Iterate through columns for the current account
                        for col_index in range(start_col, end_col):
                            # Get the bets for the current column
                            bets = df.iloc[:, col_index]

                            # Iterate through rows and place bets
                            for j, bet in enumerate(bets):
                                # Use the value from the corresponding column and row
                                url = urls[j]  # Use the URL corresponding to the current row
                                print(f'Account: {username}, URL: {url}, Column: {col_index + 1}, Row: {j + 1}, Bet: {bet}')
                                try:
                                    placebet(url, bet, username, password)
                                except Exception as e:
                                    print(f'Error placing bet: {e}')

                                time.sleep(2)

        

                                # Execute the betslip function after completing all URLs for a column
                            execute_bet()
                    
                            
                            # cashout_func()
                    except Exception as e:
                        print(e)
                    logout()
        # elif website == "Xbet":
        #     if excel_file:
        #         df = pd.read_excel(excel_file)
        #         csv_file = "output.csv"
        #         df.to_csv(csv_file, index=False)
        #         options = Options()
        #         options.add_argument('--disable-gpu')
        #         # options.add_argument('--headless')
        #         browser = webdriver.Chrome()

        #         # 1xbet login xpaths
        #         xPathLogin = '//*[@id="curLoginForm"]/span'
        #         xPathEmail = '//*[@id="username"]'
        #         xPathPassword = '//*[@id="username-password"]'
        #         xPathSubmitLogin = '//*[@id="modals-container"]/div/div/div[2]/div/div[1]/form/button/span/span/span'

        #         # 1xbet login successful confirmation xpath
        #         xPathMyAccount = '//*[@id="app"]/div[3]/header/div/div[1]/div/div/div/button[2]/span/span[1]/span[1]/span[1]'

        #         # 1xbet currency confirmation xpath
        #         xPathConfirmCurrency = '//*[@id="approve_accept"]'

        #         # Baccarat navigation xpaths
        #         xPathIframe = '//*[@id="game-iframe"]'
        #         xPathBaccart = '//div[@data-game="baccarat"]'
        #         xPathIframeGame = '//*[@id="container"]/div/div/iframe'
        #         xPathSpeedBaccartB = '//div[@data-tableid="lv2kzclunt2qnxo5"]'

        #         # Baccarat game status xpaths
        #         xPathPlaceBets = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[1]/div/div/div[contains(string(), "PLACE YOUR BETS")]'
        #         xPathPlayerWon = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[1]/div/div/div[contains(string(), "PLAYER WINS")]'
        #         xPathBankWon = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[1]/div/div/div[contains(string(), "BANKER WINS")]'
        #         xPathTie = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[1]/div/div/div[contains(string(), "TIE")]'
        #         xPathPlayerBankTie = xPathPlayerWon + '|' + xPathBankWon + '|' + xPathTie
        #         xPathWaitForNextGame = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[1]/div/div/div[contains(string(), "WAIT FOR NEXT GAME")]'

        #         # Baccarat bet placing xpaths
        #         xPath1Dollar = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[3]/div/div/div/div[1]/div/ul/li[2][div/span[contains(text(), "$ 1")]]'
        #         xPathDouble = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[3]/div/div/div/div[1]/div/ul/li[button/span[contains(text(), "DOUBLE")]]'
        #         xPathPlayerSubmit = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[2]/div/div/div/div[1]/div[1][contains(@class, "player--3F1-C")]'
        #         xPathBankSubmit = '//*[@id="root"]/div/div[1]/div/div/div[6]/div[3]/div/div[2]/div/div/div/div[1]/div[2][contains(@class, "banker--11HzV")]'

        #         # load configurations from  config.ini
        #         config = configparser.ConfigParser()
        #         config.read('config.ini')
        #         email = config.get('LoginCredentials', 'Email')
        #         password = config.get('LoginCredentials', 'Password')

        #         # sequence = config.get('BotConfig', 'BetPattern').split(",")
        #         # betInitial = int(config.get('BotConfig', 'InitialBet'))
        #         # betUpperLimit = int(config.get('BotConfig', 'upperLimit'))

        #         def login():
        #             time.sleep(5)
        #             browser.find_element(By.XPATH, xPathLogin).click()
        #             time.sleep(3)
        #             browser.find_element(By.XPATH,
        #                                  '//*[@id="modals-container"]/div/div/div[2]/div/div[1]/ul/li[2]/label/div/span[2]/span').click()
        #             time.sleep(1)
        #             usernameEl = browser.find_element(By.XPATH, xPathEmail)
        #             passwordEl = browser.find_element(By.XPATH, xPathPassword)
        #             usernameEl.send_keys(selected_account)
        #             time.sleep(1)
        #             passwordEl.send_keys(password)
        #             time.sleep(1)
        #             browser.find_element(By.XPATH, xPathSubmitLogin).click()
        #             WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, xPathMyAccount)))

        #         # navigate to login page
        #         url = 'https://1xbet.com.gh/betsonyour/line/football/1436987-ghana-division-1/190417924-young-redbull-venomous-vipers'
        #         browser.get(url)

        #         login()
        #         time.sleep(1000)
        # else:
        #     if excel_file:
        #         df = pd.read_excel(excel_file)
        #         csv_file = "output.csv"
        #         df.to_csv(csv_file, index=False)
        #         options = Options()
        #         options.add_argument('--disable-gpu')
        #         # options.add_argument('--headless')
        #         browser = webdriver.Chrome()
        #         browser.maximize_window()
        #         # 1xbet login xpaths
        #         xPathLogin = '//*[contains(concat( " ", @class, " " ), concat( " ", "font-weight-black", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "v-btn__content", " " ))]'
        #         xPathEmail = './/input[@placeholder="Mobile Number"]'
        #         xPathPassword = './/input[@placeholder="Password"]'
        #         xPathSubmitLogin = '//*[contains(concat( " ", @class, " " ), concat( " ", "font-weight-black", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "v-btn__content", " " ))]'

        #         # 1xbet login successful confirmation xpath
        #         xPathMyAccount = '//*[@id="app"]/div/div[1]/header/div[1]/div[3]/div/button[2]/span'

        #         # #load configurations from  config.ini
        #         # config = configparser.ConfigParser()
        #         # config.read('config.ini')
        #         # email = config.get('LoginCredentials', 'Email')
        #         # password = config.get('LoginCredentials', 'Password')
        #         # # sequence = config.get('BotConfig', 'BetPattern').split(",")
        #         # # betInitial = int(config.get('BotConfig', 'InitialBet'))
        #         # # betUpperLimit = int(config.get('BotConfig', 'upperLimit'))

        #         def placebet():
        #             browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #             time.sleep(4)
        #             correct_score = browser.find_element(By.XPATH, "//*[text()='Correct Score ']")
        #             correct_score.click()
        #             # time.sleep(200)
        #             print('correct score dropdown click')
        #             time.sleep(3)

        #             table = browser.find_elements(By.XPATH, ".//div[@data-test-id='market-body-base-component']")
        #             # Read values from the CSV file and store them in a list
        #             search_values = []

        #             # Specify the path to your CSV file
        #             csv_file_path = 'D:/sarabjit/2023/betting (2)/bots/bets.csv'

        #             # Read values from a specific column in the CSV file
        #             with open(csv_file_path, 'r') as csvfile:
        #                 reader = csv.DictReader(csvfile)
        #                 for row in reader:
        #                     search_values.append(row['A'])  # Replace 'column_name' with the actual column name in your CSV

        #             # Find all the elements in the table with the specified XPath
        #             bets = table[-1].find_elements(By.XPATH, ".//span[@class='outcome-text']")

        #             for bet in bets:
        #                 if bet.text in search_values:
        #                     print(bet.text)
        #                     bet.click()

        #             print(search_values)
        #             # input count4
        #             # time.sleep(400)
        #             # Scroll to the top of the page using JavaScript
        #             browser.execute_script("window.scrollTo(0, 0);")
        #             count = browser.find_element(By.XPATH, './/input[@class="text-right input text-body-1"]')
        #             count.click()
        #             count.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
        #             count.send_keys(Keys.BACKSPACE)
        #             count.send_keys('0.5')
        #             time.sleep(5)
        #             # click confirm bet
        #             place = browser.find_element(By.XPATH, '//*[@id="betNowBtn"]')
        #             place.click()
        #             print('place bet click')
        #             time.sleep(7)

        #             ok = browser.find_elements(By.XPATH,
        #                                        '//*[contains(concat( " ", @class, " " ), concat( " ", "primary", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "v-btn__content", " " ))]')[
        #                 -1]
        #             ok.click()
        #             time.sleep(4)

        #             # #click mybet
        #             mybet = browser.find_element(By.XPATH,
        #                                          "//*[@id='app']/div/div[1]/header/div[2]/div/div/div[2]/div/button[2]")
        #             mybet.click()
        #             time.sleep(5)
        #             cashout_count = browser.find_elements(By.XPATH,
        #                                                   '//*[@id="2"]/div/div/div[2]/div/div/div/div/div[1]/div[3]/span/div/div[1]/div[2]/button[1]')
        #             print('cashout_count :', len(cashout_count))
        #             if len(cashout_count) >= 1:
        #                 for i in range(0, len(cashout_count)):
        #                     try:
        #                         browser.find_elements(By.XPATH, '')[i].click()
        #                     except:
        #                         browser.find_element(By.XPATH,
        #                                              '//*[@id="2"]/div/div/div[2]/div/div/div/div/div[1]/div[3]/span/div/div[1]/div[2]/button[1]').click()
        #                     time.sleep(3)

        #                     cashout_confirm = browser.find_element(By.XPATH, '//*[@id="0"]/div/div[2]/button[2]/span/span')
        #                     cashout_confirm.click()
        #                     time.sleep(3)
        #                     try:
        #                         close = browser.find_element(By.XPATH,
        #                                                      '//*[@id="app"]/div[4]/main/div[2]/div/div/div/div[2]/button')
        #                         close.click()

        #                     except:
        #                         pass

        #                     time.sleep(3)

        #                     print(f'Cashout done {i}')

        #         def login():
        #             # browser.find_element(By.XPATH,'//*[@id="modals-container"]/div/div/div[2]/div/div[1]/ul/li[2]/label/div/span[2]/span').click()
        #             time.sleep(1)
        #             usernameEl = browser.find_element(By.XPATH, xPathEmail)
        #             passwordEl = browser.find_element(By.XPATH, xPathPassword)
        #             usernameEl.send_keys(selected_account)
        #             time.sleep(1)
        #             passwordEl.send_keys(password)
        #             time.sleep(1)
        #             browser.find_element(By.XPATH, xPathSubmitLogin).click()
        #             WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, xPathMyAccount)))

        #         # navigate to login page
        #         url = 'https://www.betway.com.gh/event/soccer/england/fa-cup/barnsley-fc-horsham-fc/?eventId=12510822&fixtureType=live'
        #         browser.get(url)

        #         login()
        #         time.sleep(3)
        #         placebet()
        #         time.sleep(1000)
            execute()
        return JsonResponse(response_data)
def get_account_choices(request):
    accounts = UserAccount.objects.all().values_list('username', flat=True)
    return JsonResponse({'accounts': list(accounts)})
