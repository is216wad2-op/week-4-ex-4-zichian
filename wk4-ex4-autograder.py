import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')  # Run headlessly
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Update to the path or URL of your solution HTML file
url = 'file://' + os.path.abspath('ex4.html')
driver.get(url)
time.sleep(1)  # wait for page to load

def get_list_items():
    ul = driver.find_element(By.ID, "myul")
    return [li.text.replace("delete", "").strip() for li in ul.find_elements(By.TAG_NAME, "li")]

# Verify initial items
expected_initial = ["Notebook", "Jello", "Spinach", "Rice", "Birthday Cake", "Candles"]
assert get_list_items() == expected_initial, "Initial list items incorrect."

# Add item with button click
input_box = driver.find_element(By.ID, "userinput")
enter_button = driver.find_element(By.ID, "enter")

new_item_1 = "Apples"
input_box.send_keys(new_item_1)
enter_button.click()
time.sleep(0.5)

items_after_click = get_list_items()
assert new_item_1 in items_after_click, "New item not added by button click."
assert input_box.get_attribute('value') == '', "Input box not cleared after button click."

# Add item with Enter key press
new_item_2 = "Oranges"
input_box.send_keys(new_item_2)
input_box.send_keys(Keys.ENTER)
time.sleep(0.5)

items_after_enter = get_list_items()
assert new_item_2 in items_after_enter, "New item not added by Enter key."

# Test deleting the last added item ("Oranges")
ul = driver.find_element(By.ID, "myul")
# Find the last <li> which should have "Oranges" text
last_li = ul.find_elements(By.TAG_NAME, "li")[-1]
delete_button = last_li.find_element(By.TAG_NAME, "button")
delete_button.click()
time.sleep(0.5)

items_after_delete = get_list_items()
assert new_item_2 not in items_after_delete, "Delete button did not remove the item."

print("All tests passed!")

driver.quit()
