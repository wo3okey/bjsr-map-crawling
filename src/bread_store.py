import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import sheet


def end_system():
    print('>> end of system')
    driver.close()


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('lang=ko_KR')
    # chrome_options.headless = True
    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return chrome_driver


# set driver
driver = set_chrome_driver()
driver.get('https://map.kakao.com/')

# set search keyword
elem = driver.find_element(By.NAME, "q")
elem.send_keys("미사 피자")
elem.send_keys(Keys.RETURN)

# remove guild popup
driver.find_element(By.CSS_SELECTOR, ".tit_coach").click()
time.sleep(1)

# result
result = driver.find_element(By.ID, "info.search.place")
if "HIDDEN" in result.get_attribute("class"):
    print(">> no search result")
    end_system()

has_next = True
cur_page_num = 1
next_btn = driver.find_element(By.ID, "info.search.page.next")

# click more btn
try:
    more_button = driver.find_element(By.ID, "info.search.place.more").click()
    time.sleep(3)
except ElementNotInteractableException:
    print(">> just one page")
    place_list = driver.find_element(By.ID, "info.search.place.list")
    end_system()

# search result - around pages
name_cell_value = set()
tel_cell_value = set()
address_cell_value = set()

while has_next:
    for page in range(1, 6):
        try:
            # find page
            driver.find_element(By.ID, "info.search.page.no" + str(page)).click()
            time.sleep(3)

            # crawling
            place_list = driver.find_elements(By.ID, "info.search.place.list")
            place_html = place_list[0].get_attribute('innerHTML')
            place_info = BeautifulSoup(place_html, "html.parser")
            size = place_info.find_all('li').__len__() - 1

            print("page: " + str(cur_page_num))
            for idx in range(0, size):
                place_name = place_info.select('.head_item > .tit_name > .link_name')[idx].text
                name_cell_value.add(place_name)

                place_tel = place_info.select('.info_item > .contact > span')[idx].text
                tel_cell_value.add(place_tel)

                place_address = place_info.select('.info_item > .addr > p')[idx].text
                address_cell_value.add(place_address)

                print(place_name + " | " + place_address + " | " + place_tel)

            cur_page_num += 1
            print()

        except ElementNotInteractableException:
            print('>> end of page')
            break

    has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
    if not has_next:
        print(">> update excel sheet...")
        sheet.write_cells("name", name_cell_value)
        sheet.write_cells("tel", tel_cell_value)
        sheet.write_cells("address", address_cell_value)

        end_system()
        break
    else:
        next_btn.click()
