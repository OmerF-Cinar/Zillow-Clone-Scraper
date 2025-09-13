from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://appbrewery.github.io/Zillow-Clone/")

items_tag = driver.find_element(By.XPATH, "//*[@id='grid-search-results']/ul")
wait = WebDriverWait(driver, 20)

items = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, "//*[@id='grid-search-results']/ul/li")
))

address_list = []
price_list = []
bd_list = []
ba_list = []
sqft_list = []

for item in items:
    try:
        address = item.find_element(By.XPATH, ".//a/address").text.strip()

        price = item.find_element(By.CSS_SELECTOR, "span[data-test='property-card-price']").text.strip()

        beds, baths, sqft = None, None, None

        details_div = item.find_element(By.CSS_SELECTOR, "div.StyledPropertyCardDataArea-dbDWjx")
        details = details_div.find_elements(By.CSS_SELECTOR, "ul.StyledPropertyCardHomeDetailsList li")

        for detail in details:
            num = detail.find_element(By.TAG_NAME, "b").text.strip()
            label = detail.find_element(By.TAG_NAME, "abbr").text.strip()

            if label == "bd":
                beds = num
            elif label == "ba":
                baths = num
            elif label == "sqft":
                sqft = num
                
        address_list.append(address)
        price_list.append(price)
        bd_list.append(beds)
        ba_list.append(baths)
        sqft_list.append(sqft)

    except Exception as e:
        print("Error:", e)

with open("zillow_listings.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Address", "Price", "Bedrooms", "Bathrooms", "Squarefeet"])

    for i in range(len(address_list)):
        writer.writerow([address_list[i], price_list[i], bd_list[i], ba_list[i], sqft_list[i]])
