from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


# Set up Firefox options

options = Options()
options.headless = True  # Run in headless mode 

# explicitly point to the geckodriver path
service = Service("/usr/local/bin/geckodriver")

# launch browser
driver = webdriver.Firefox(service=service, options=options)

driver.set_window_position(0, 0)
driver.set_window_size(960, 1080)

driver.get("https://riyasewana.com/search/motorcycles")

time.sleep(2)


#setting the maxium year as 2005

driver.find_element(by='xpath', value='//*[@id="year_max"]/option[22]').click()
time.sleep(2)

#setting the model as CD 125 as for Honda CD 125

input_element = driver.find_element(by='xpath', value='//*[@id="model"]')
time.sleep(2)
input_element.click()
input_element.send_keys('CD 125')
time.sleep(2)

#click search

search_button = driver.find_element(by='xpath', value='//*[@id="srch_btn"]')
search_button.click()
time.sleep(2)

#getting the modified link

new_link = driver.current_url
print(new_link)
time.sleep(2)

#finding the ads on the first page

ads = driver.find_elements(By.XPATH, '//*[@id="content"]/ul/li')
print(f"found {len(ads)}.ads")

#exporting ad urls to a list

url_list = []

for ad in ads:
    ad_link = ad.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    #print(ad_link)
    url_list.append(ad_link)
    print(url_list)

#combing through the list and getting the table informaiton like price, contact info., condition, year, etc...

for ad_link in url_list:
    driver.get(ad_link)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', class_='moret')

    if table:
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['tr', 'td']):
                row_data.append(cell.get_text(strip=True))
            print(row_data)
            
    else:
        print("Table not found")
        
    time.sleep(2)

driver.quit()
