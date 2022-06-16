# amazon product price alert through email. This can be automated in cloud platforms like pythonanywhere to run periodically.
# program is accessing the price of a product on amazon, and notifies through email if the price is lower than a desired price

import requests
from bs4 import BeautifulSoup
import lxml
import smtplib


# Get product details from amazon

URL = "https://www.amazon.co.uk/Samsung-Galaxy-Smartphone-Android-Phantom/dp/B08QN9QHP4/ref=sr_1_8?crid=YSO5PDFDEGF3&keywords=s22&qid=1655311684&sprefix=s22%2Caps%2C136&sr=8-8"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ro;q=0.7"
}
response = requests.get(URL, headers=header)
soup = BeautifulSoup(response.content, "lxml")
#print(soup.prettify())

# inspect HTML price element and retrieve the price
price = soup.find(class_="a-price-whole").get_text()
price_as_float = float(price)

title = soup.find(id="productTitle").get_text().strip()  # retrieve product title

# send notification email if the price is lower than desired price
BUY_PRICE = 600 # desired price
email_Address = "*"
if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"
    # gmail configuration
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(email_Address, password="*")
        connection.sendmail(
            from_addr=email_Address,
            to_addrs=email_Address,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}"
        )
        print("Price alert submitted")
else:
    print("Item price too high!")