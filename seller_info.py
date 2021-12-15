from selenium import webdriver 
from time import sleep
from selenium.webdriver.common.keys import Keys

class OKCBot():
    def __init__(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path=PATH,options=chrome_options)

    def open(self):
        self.driver.get('http://shopee.co.id/')

    def login(self):
        email = self.driver.find_element_by_xpath('//*[@id="basic_email"]')
        email.send_keys('sarveshdubey@credicxo.com')
        email.click()

        password = self.driver.find_element_by_xpath('//*[@id="basic_password"]')
        password.send_keys('Ilmskvians')
        password.click()

        login = self.driver.find_element_by_xpath('//*[@id="basic"]/div[4]/div/div/div/button')
        login.click()
        sleep(3)

    def get_sellers(self):
        keyword = self.driver.find_element_by_xpath('//*[@id="rc_select_0"]')
        keyword.send_keys("Seller")
        keyword.click()

        sleep(1)

        country = self.driver.find_element_by_xpath('//*[@id="rc_select_1"]')
        country.send_keys("Indonesia")
        country.click()

        sleep(1)

        search = self.driver.find_element_by_xpath('//*[@id="root"]/div/section/main/div/div[1]/div[2]/div[2]')
        search.click()

    def get_cards(self):
        sleep(3)
        try:
            cards = self.driver.find_elements_by_class_name('card h-100')
            sleep(2)
        except:
            pass  

    



