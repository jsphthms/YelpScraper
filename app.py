from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from locators import Locators

import json

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--headless")


class ScrapeYelp:
    def __init__(self):
        self.chrome = webdriver.Chrome(
            executable_path="/Users/Joseph/Projects/chromedriver", options=options
        )
        self.businesses = []
        self.counter = 0

    def goto_site(self):
        self.chrome.get("https://yelp.com")

    def find_biz(self, *args):
        self.chrome.implicitly_wait(5)
        inputFind = self.chrome.find_element_by_xpath('//*[@id="find_desc"]')
        inputFind.send_keys(category)

        self.chrome.implicitly_wait(5)
        inputLocation = self.chrome.find_element_by_xpath('//*[@id="dropperText_Mast"]')
        for i in range(30):
            inputLocation.send_keys(Keys.BACKSPACE)
        inputLocation.send_keys(city)
        inputLocation.send_keys(Keys.ENTER)

    def get_data(self):
        self.chrome.implicitly_wait(5)
        for i in range(6, 16):
            clickLocation = self.chrome.find_element_by_xpath(
                f'//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/ul/li[{i}]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a'
            )
            clickLocation.click()

            try:
                name = self.chrome.find_element_by_xpath(Locators.NAME[0]).text
            except NoSuchElementException:
                pass
                name = ""

            try:
                website = self.chrome.find_element_by_xpath(Locators.WEBSITE[0]).text
            except NoSuchElementException:
                try:
                    website = self.chrome.find_element_by_xpath(
                        Locators.WEBSITE[1]
                    ).text
                except NoSuchElementException:
                    pass
                    website = ""
            try:
                phone_number = self.chrome.find_element_by_xpath(
                    Locators.PHONE_NUMBER[0]
                ).text
            except NoSuchElementException:
                try:
                    phone_number = self.chrome.find_element_by_xpath(
                        Locators.PHONE_NUMBER[1]
                    ).text
                except NoSuchElementException:
                    try:
                        phone_number = self.chrome.find_element_by_xpath(
                            Locators.PHONE_NUMBER[2]
                        ).text
                    except NoSuchElementException:
                        pass
                        phone_number = ""

            try:
                add1 = self.chrome.find_element_by_xpath(Locators.ADD_LINE1[0]).text
            except NoSuchElementException:
                try:
                    add1 = self.chrome.find_element_by_xpath(Locators.ADD_LINE1[1]).text
                except NoSuchElementException:
                    pass
                    add1 = ""

            try:
                add2 = self.chrome.find_element_by_xpath(Locators.ADD_LINE2[0]).text
            except NoSuchElementException:
                try:
                    add2 = self.chrome.find_element_by_xpath(Locators.ADD_LINE2[1]).text
                except NoSuchElementException:
                    pass
                    add2 = ""
            try:
                add3 = self.chrome.find_element_by_xpath(Locators.ADD_LINE3[0]).text
            except NoSuchElementException:
                try:
                    add3 = self.chrome.find_element_by_xpath(Locators.ADD_LINE3[1]).text
                except NoSuchElementException:
                    try:
                        add3 = self.chrome.find_element_by_xpath(
                            Locators.ADD_LINE3[2]
                        ).text
                    except NoSuchElementException:
                        add3 = ""

            address = add1 + ". " + add2 + ". " + add3

            biz = {
                "name": name,
                "website": website,
                "phone_number": phone_number,
                "address": address,
            }

            self.businesses.append(biz)

            self.counter += 1
            print(self.counter)
            self.chrome.back()

        return self.businesses


category = input("What would you like to look for? ")
city = input("In what city? ")

scrape = ScrapeYelp()
scrape.goto_site()
scrape.find_biz(category, city)
businesses = scrape.get_data()

with open("targets.json", "w") as json_file:
    data = {}
    data[category] = []
    for biz in businesses:
        data[category].append(biz)
    json.dump(data, json_file, sort_keys=False, indent=4)
