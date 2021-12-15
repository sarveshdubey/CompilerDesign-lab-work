from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from configure import *
from time import sleep
import random
import os
import csv
from datetime import datetime


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


def create_csv(data, date):
    filename = 'Linked-In-' + date + '.csv'
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    csvFile.close()


def add_to_csv(data, date):
    filename = 'Linked-In-' + date + '.csv'
    with open(filename, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    csvFile.close()


def send_invitation_note(browser):
    note_button_entity = browser.find_element_by_xpath('//*[@id="artdeco-modal-outlet"]/div/div/div[3]/button')
    note_button_entity.click()
    sleep(1)
    message = browser.find_element_by_xpath('//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/textarea')
    message.send_keys(CONNECT_MESSAGE)
    sleep(1)
    send_buttom_entity = browser.find_element_by_xpath('//*[@id="artdeco-modal-outlet"]/div/div/div[3]/button[2]')
    send_buttom_entity.click()
    return browser


def connect_buttons(browser):
    for _ in range(PEOPLE_PER_PAGE):
        # check if the button's text is (button, follow or message)
        button_entity = browser.find_element_by_xpath(
            '//*[@class="reusable-search__entity-results-list list-style-none"]/li[1]/div/div/div[3]/button')
        __text__be = button_entity.text
        if 'Connect' in __text__be:
            button_entity.click()
            browser = send_invitation_note(browser)
            sleep(random.uniform(2, 8))


def connect(browser):
    date = str(datetime.now().date())
    if not os.path.exists('Linked-In-' + date + '.csv'):
        create_csv(["Name", "Title", "Title Match", "url", "Current Company", "Connected"], date)

    for keyword in SEARCH_KEYWORDS:
        for page in range(1, int(MAX_LIMIT // PEOPLE_PER_PAGE) + 1):
            browser.get(
                f'https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=SWITCH_SEARCH_VERTICAL&page={page}')
            connect_buttons(browser)

    return browser


def main():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=chrome_options)

    """ SIGN IN """
    browser = sign_in(browser=browser)
    """ CONNECT WITH USERS"""
    browser = connect(browser=browser)
    sleep(10)


if __name__ == "__main__":
    if DEBUG:
        try:
            main()
        except Exception:
            import traceback

            traceback.print_exc()
    else:
        main()
