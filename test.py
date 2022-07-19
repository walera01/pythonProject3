from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv

# driver = webdriver.Firefox()
# driver.get("url")
# element = driver.find_element_by_css_selector()
# element.click()

headers = {
    "Accept" : "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
url = "https://myfin.by/currency/rechitsa"

req = requests.get(url, headers=headers)

src = req.text

# with open('index.html', 'w', encoding="utf-8")as file:
#     file.write(src)

# with open("index.html", 'r', encoding="utf-8") as file:
#     src = file.read()

soup = BeautifulSoup(src, "lxml")
print("-"*50)

hat_bank = soup.find(class_='head-sort arrow')
print(hat_bank.text)

hat_currency = soup.find_all('th', class_='cur-name')
print("-"*50)
print(hat_currency[0].text)
for i in hat_currency:
    print(i.text)



product_info = []
    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )