from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from selenium.webdriver import Keys
from .models import UserAccount
from .forms import UserAccountForm
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains
import time,csv,logging,io,json
from selenium.webdriver.chrome.options import Options


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
    clear_csv()
    return render(request, 'accounts/execute.html')


@csrf_exempt
def upload_excel(request):
    if request.method == 'POST':
        selected_bot = request.POST.get('selected_bots')
        urls = [request.POST.get(f'urlBot{selected_bot}{i}') for i in range(1, 8)]
        uploaded_file = request.FILES['excelFile']
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
            # print(accounts)
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
                    # WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, xPathMyAccount)))
                    # time.sleep(2)
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
                # print(bet_columns)

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
                try:
                    confirm = browser.find_element(By.XPATH, "//*[text()='Confirm']") #not
                    confirm.click()
                    time.sleep(3)
                except:
                    pass
                try:
                    ok = browser.find_element(By.XPATH, "//*[text()='OK']") #not
                    ok.click()
                    time.sleep(1)
                except:
                    pass
                try:
                    Insufficient_Balance =  browser.find_element(By.XPATH, "//span[contains(text(), 'Balance Insufficient')]")
                    print("=========================Insuffient Balance=========================================")
                except:
                    pass
                
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
                                                    '//*[@id="j_betslip"]/div[3]/ul/li/div[2]/div[4]/div[2]/div[5]/button') #not
                        cashout.click()
                        time.sleep(1)
                        cashout_confirm = browser.find_element(By.XPATH,
                                                            '//*[@id="j_betslip"]/div[3]/ul/li/div[2]/div[4]/div[2]/div[1]/div[2]/button[2]/span/span') #not
                        cashout_confirm.click()
                        time.sleep(3)
                        print(f'Cashout done {i}')

            def execute_sportybet():
                
                csv_file_path = uploaded_file
                results = []
                df = pd.read_csv(csv_file_path, header=None)
                total_rows, total_columns = df.shape
                # print(uploaded_file)
                # print(total_rows)
                # print(total_columns)
                all_results = []
                # print('sportBet_accounts',len(sportBet_accounts))
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
                                
                                if url != '':
                                    data = [{'Bet': bet}] 
                                    csv_file_path = 'Sportybet.csv'
                                    with open(csv_file_path, 'a', newline='') as csv_file:
                                        csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                                        # Check if the file is empty (no header) and write the header if needed
                                        if csv_file.tell() == 0:
                                            csv_writer.writeheader()
                                        csv_writer.writerows(data)
                                    print(f'CSV file "{csv_file_path}" has been updated.')

                                    print("############################################################################################")
                                    print("====================================",bet,"===============================================")
                                    print("############################################################################################")
                                try:
                                    placebet(url, bet, username, password)
                                except:
                                    # print(f'Error placing bet: {e}')
                                    pass
                                time.sleep(2)
                                # Execute the betslip function after completing all URLs for a column
                            execute_bet()
                            # cashout_func()
                    except Exception as e:
                        print(e)
                    logout()
                    clear_csv()          
            execute_sportybet()
            

        return JsonResponse(response_data)
    

def get_account_choices(request):
    accounts = UserAccount.objects.all().values_list('username', flat=True)
    return JsonResponse({'accounts': list(accounts)})

def json_data(request):
    csv_file_path = 'Sportybet.csv'
    try:
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            print(f"Column names: {csv_reader.fieldnames}")
            # Read rows into a list
            data_list = [row for row in csv_reader]
        return JsonResponse({'data': data_list})
    except FileNotFoundError:
        return JsonResponse({'error': 'CSV file not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error reading CSV: {e}'}, status=500)
    
def clear_csv(file_path='Sportybet.csv'):
    with open(file_path, 'w', newline='') as csvfile:
        pass


def submit_data(request):
    if request.method == 'POST':
        try:
            clear_csv()
            return JsonResponse({'message': 'CSV file cleared successfully'})
        except Exception as e:
            return JsonResponse({'message': f'Error clearing CSV file: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)