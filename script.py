# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from configure import *
from time import sleep
import csv
from datetime import datetime
import random
import os

# %%
def sign_in(browser):
    browser.get('https://linkedin.com/uas/login')
    emailElement = browser.find_element_by_id('username')
    emailElement.send_keys(EMAIL)
    passElement = browser.find_element_by_id('password')
    passElement.send_keys(PASS)
    passElement.submit()

    if PRINT_ACTIONS:
        print('-> Signing in...')
    sleep(3)
    print('!!! Sign in success!\n')
    return browser

# %%
def create_csv(data, date):
    filename = 'Linked-In-' + date + '.csv'
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)


def add_to_csv(data, date):
    filename = 'Linked-In-' + date + '.csv'
    with open(filename, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)

# %%
def send_invitation_note(browser):
    note_button_entity = browser.find_element_by_xpath('//button[@aria-label="Add a note"]')
    note_button_entity.click()
    sleep(1)
    message = browser.find_element_by_xpath('//textarea[@name="message"]')
    message.send_keys(CONNECT_MESSAGE)
    sleep(1)
    send_buttom_entity = browser.find_element_by_xpath('//button[@aria-label="Send now"]')
    send_buttom_entity.click()
    return browser

# %%
def connect_buttons_fetch_details(browser, keyword):
    global NO_OF_CONNECTIONS
    results = browser.find_elements_by_class_name('reusable-search__result-container')
    for result in results:
        profile = result.find_elements_by_class_name('app-aware-link')[1]
        profile_link = profile.get_attribute('href')
        profile_name = profile.text.split('\n')[0]
        title = result.find_element_by_class_name('entity-result__primary-subtitle').text
        place = result.find_element_by_class_name('entity-result__secondary-subtitle').text
        profile_row = [profile_name, title, keyword, profile_link, place, 'False']
        button_entity = result.find_element_by_css_selector('.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')
        __text__be = button_entity.text
        if 'Connect' in __text__be:
            sleep(2)
            try:
                button_entity.click()
            except Exception:
                continue
            browser = send_invitation_note(browser)
            sleep(random.uniform(1, 2))
            NO_OF_CONNECTIONS = NO_OF_CONNECTIONS - 1
            print(NO_OF_CONNECTIONS)
            add_to_csv(data=profile_row, date=str(datetime.now().date()))

def connect(browser):
    global NO_OF_CONNECTIONS
    page_counter = 1
    date = str(datetime.now().date())
    if not os.path.exists('Linked-In-' + date + '.csv'):
        create_csv(["Name", "Title", "Title Match", "Profile Link", "Place", "Connected"], date)

    for keyword in SEARCH_KEYWORDS:
        while NO_OF_CONNECTIONS != 0:
            browser.get(
                f'https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=SWITCH_SEARCH_VERTICAL&page={page_counter}')
            connect_buttons_fetch_details(browser, keyword)
            page_counter += 1
    return browser

# %%

chrome_options = Options()
if HEADLESS:
    chrome_options.add_argument('--headless')
chrome_options.add_argument("--start-maximized")

browser = webdriver.Chrome( executable_path=r"C:\Program Files (x86)\chromedriver" ,options=chrome_options)

""" SIGN IN """
browser = sign_in(browser=browser)
""" CONNECT WITH USERS"""
# browser = connect(browser=browser)
# sleep(10)

# %%
browser.get('https://www.linkedin.com/search/results/people/?keywords=fintech&origin=SWITCH_SEARCH_VERTICAL&page=11')


# %%
results = browser.find_elements_by_xpath('//li[@class="reusable-search__result-container "]')

# %%
for i in results:
    # x  = i.find_element_by_xpath('//*[@class="artdeco-button" or @class="artdeco-button--2" or @class="artdeco-button--secondary"]')
    x = i.find_element_by_css_selector(".artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view")
    # x = i.find_element_by_class_name('artdeco-button')
    print(x.text)
    # print(i.find_element_by_class_name('artdeco-button').text)

# %%
browser = connect(browser)

# %%



