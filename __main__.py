import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telegram_send

from scripts.amazon_product import Product

if __name__ == '__main__':
    BASE_URL = 'https://www.amazon.com.br/PlayStation-Console-PlayStation%C2%AE5/dp/B088GNRX\
        3J/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=ps5&qid=\
        1613470308&sr=8-1'
    BASE_URL = 'https://www.amazon.com.br/God-War-Hits-PlayStation-4/dp/B07YT1GLV9/?_encoding=\
        UTF8&pd_rd_w=yRrM3&pf_rd_p=d2ea4cd9-b3fa-4bdb-ab83-24ca9c54ecbe&pf_rd_r=3JF03Z0NMXW0PXV\
        M86Z1&pd_rd_r=b592df2f-51e0-4fe5-8ccd-e6ff9930134e&pd_rd_wg=CLvfl&ref_=pd_gw_ci_mcx_mr_hp_d'

    product = Product(BASE_URL)

    DRIVER_PATH = os.path.abspath('drivers/chromedriver')
    # Set the driver options
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # linux only
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        executable_path=DRIVER_PATH, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(BASE_URL)

    product.name = product.get_product_feature(
        driver, 'span', 'id', 'productTitle')
    product.price = product.get_product_feature(
        driver, 'span', 'id', 'priceblock_ourprice')

    if not product.name:
        telegram_send.send(
            messages=["Ocorreu um erro ao buscar o produto, verificar no site"])

    if product.price:
        if product.name:
            telegram_send.send(messages=[
                f"Produto {product.name} encontrado por {product.price} na \
                url abaixo: \n\n {product.url}"])
        else:
            telegram_send.send(messages=[
                f"Produto encontrado por {product.price} na url abaixo: \n\n {product.url}"])

    driver.quit()

    current_date = datetime.now()
    current_hour = current_date.hour
    current_minute = current_date.minute

    # Checks if bot has run for 24h (every 7 am)
    if current_hour == 9 and current_minute <= 1:
        telegram_send.send(
            messages=["Bot ativo por 24h, produto ainda não encontrado"])
