from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException as eleec
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get('https://store.steampowered.com/')
parent_ele_loc = (By.CLASS_NAME, 'tab_content_items')


def get_child_elements(parent_locator):
    parent_element = WebDriverWait(driver, 300).until(ec.presence_of_element_located(parent_locator))
    return parent_element.find_elements(By.TAG_NAME, 'a')


main_elements = get_child_elements(parent_ele_loc)
name = []
price = []

for j, i in enumerate(range(len(main_elements))):
    multi = 0
    parent_ele = get_child_elements(parent_ele_loc)[i]
    price.append(parent_ele.find_element(By.CLASS_NAME, 'discount_final_price').text.strip())
    parent_ele.click()
    try:
        age_check = driver.find_element(By.CLASS_NAME, 'agegate_birthday_selector')
    except eleec:
        age_check = 0

    if age_check:
        multi += 1
        day = age_check.find_element(By.ID, 'ageDay')
        day.click()
        select = Select(day)
        select.select_by_visible_text('22')

        month = age_check.find_element(By.ID, 'ageMonth')
        month.click()
        select = Select(month)
        select.select_by_visible_text('September')

        year = age_check.find_element(By.ID, 'ageYear')
        year.click()
        select = Select(year)
        select.select_by_visible_text('2005')

        submit = driver.find_element(By.ID, 'view_product_page_btn')
        submit.click()
    try:
        name.append(WebDriverWait(driver, 60).until(
            ec.presence_of_element_located((By.ID, 'appHubAppName'))
        ).text.strip())

    except TimeoutException:
        continue

    if multi:
        driver.back()
    driver.back()

file_name = 'popular_steam_games.csv'
if not os.path.isfile(file_name):
    data = {
        'Name': name,
        'Price': price
    }
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)

driver.close()

# Just in case if it becomes necessary the code to login
'''
fill = login_box.find_elements(By.CLASS_NAME, '_2eKVn6g5Yysx9JmutQe7WV')
k = 0
for i in fill:
    if k == 0:
        i.click()
        i.send_keys('') Steam id username
    else:
        i.click()
        i.send_keys('') Steam id password
    k += 1
rememberme = login_box.find_element(By.ID, 'base')
rememberme.click()

login = login_box.find_element(By.CLASS_NAME, '_2QgFEj17t677s3x299PNJQ')
login.click()
'''
