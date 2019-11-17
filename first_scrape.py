import pickle
import re

from selenium import webdriver

PROVIDER_NAME = "PG&E"
PROVIDERS = {"PG&E": "https://m.pge.com/#outages"}


driver = webdriver.Chrome('/Applications/chromedriver')
driver.get(PROVIDERS[PROVIDER_NAME])

# Find data list
elem = driver.find_element_by_link_text("SHOW CITY LIST")
elem.click()

switched = driver.switch_to.active_element

e = driver.find_element_by_class_name("pge_coc-outages-city_list_modal")
items = e.find_elements_by_class_name("cityListItem")

# Collect data
outage_data = []
for i in items:
    region = i.find_element_by_class_name("regionName").text
    info = i.find_element_by_class_name("customerAffected").text
    num_outages = int(re.search(r'(\d+) Outages', info).group(1))
    num_customers = int(re.search(r'(\d+) Customers', info).group(1))
    outage_data.append({"region": region, "outages": num_outages,
                        "customers": num_customers})

# Store data
pickle.dump(outage_data, open('outage_data.p', 'wb'))

driver.close()

