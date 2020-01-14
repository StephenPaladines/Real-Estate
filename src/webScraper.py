import time
import sys
from config import url
from googleSheet import addDataToGS
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def readData():
    with open("data/cacheID.json", "r") as read_file:
        try:
            data = json.load(read_file)
        except:
            data = {}
    return data


def findDuplexs(driver):
    # Filter options
    driver.find_element_by_xpath(
        '//*[@title="Residential Income"]').click()    # Property Type = Duplex

    driver.find_element_by_xpath(
        "//select[@id='Fm86_Ctrl1874_LB']/option[text()='$300,000']").click()  # Price Max = 300,000

    driver.find_element_by_xpath(
        '//*[@id="_ctl0_m_lnkSearch"]').click()  # Search


def main():
    webDriverLocation = "../web-driver/geckodriver.exe"

    driver = webdriver.Firefox(executable_path=webDriverLocation)

    # Seconds before timeout if element cannot be found
    driver.implicitly_wait(10)

    driver.get(url)

    time.sleep(4)
    driver.find_element_by_xpath(
        '//*[@title="Start a New Search"]').click()  # Starts a new search

    # Filter options
    #---------------------------------------------------------------------------------------#
    driver.find_element_by_xpath(
        '//*[@title="Residential Income"]').click()    # Property Type = Duplex

    driver.find_element_by_xpath(
        "//select[@id='Fm86_Ctrl1874_LB']/option[text()='$300,000']").click()  # Price Max = 300,000

    driver.find_element_by_xpath(
        '//*[@id="_ctl0_m_lnkSearch"]').click()  # Search
    #---------------------------------------------------------------------------------------#

    time.sleep(3)

    # Selects the three circle icon
    driver.find_element_by_xpath('//*[@id="_ctl0_m_lbViewList"]').click()

    # Selects Client Multi-Row Option
    driver.find_element_by_xpath('//*[text()="*Client Multi-Row"]').click()

    time.sleep(3)

    # Loads entire list of properties
    while True:
        try:
            driver.find_element_by_xpath(
                '//*[text()="See More Results"]').click()
        except:
            break

    time.sleep(2)
    list = []   # Parse through list of homes
    jsonData = {}   # Output container for json data
    sys.stdout.flush()
    container = driver.find_elements_by_xpath(
        '//table[@class="DisplayRow d236m0"]')

    for listing in container:
        mlsID = listing.find_element_by_xpath(
            './/span[@class="field formula"]').text
        # Break if cache data or current MLSID repeats
        if (jsonData.get(mlsID, -1) != -1):
            break
        addressAndDesc = listing.find_elements_by_xpath(
            './/span[@class="formula field d236m22"]')
        address = addressAndDesc[0].text
        bodyDesc = addressAndDesc[1].text
        price = int(listing.find_element_by_xpath(
            './/span[@class="field"]').text[1::].replace(',', ''))
        totalArea = listing.find_element_by_xpath(
            './/span[@class="formula"]').text.replace('¤', '')         # Removes the special character in front
        # Index 2 belongs to the year. Wrapped Field is used acrossed multiple classes hence the use of indicies
        year = int(listing.find_elements_by_xpath(
            './/span[@class="wrapped-field"]')[2].text)
        try:
            totalArea = int(totalArea.replace(',', ''))
        except:
            totalArea = 0
        listObj = {
            "mlsID": mlsID,
            "address": address,
            "bodyDesc": bodyDesc,
            "price": price,
            "totalArea": totalArea,
            "year": year
        }
        list.append(listObj)            # Append obj to list
        jsonData[mlsID] = listObj       # Append new item to dictionary
    print(jsonData)
    addDataToGS(list)
    driver.quit()


if __name__ == '__main__':
    main()
