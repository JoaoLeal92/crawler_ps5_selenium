import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telegram_send
import argparse

from scripts.amazon_product import Product

parser = argparse.ArgumentParser(description='Amazon PS5 crawler.')
parser.add_argument(
    '-r',
    '--raspi',
    type=bool,
    help='flag weather the crawler runs on a raspberry pi or not'
)
args = parser.parse_args()

if __name__ == '__main__':
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Início da operação')
    BASE_URL = 'https://www.amazon.com.br/PlayStation-Console-PlayStation%C2%AE5/dp/B088GNRX3J/ref\
        =sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=ps5&qid=1613470308&sr=8-1'
    # BASE_URL = 'https://www.amazon.com.br/God-War-Hits-PlayStation-4/dp/B07YT1GLV9/?_encoding=\
    #     UTF8&pd_rd_w=yRrM3&pf_rd_p=d2ea4cd9-b3fa-4bdb-ab83-24ca9c54ecbe&pf_rd_r=3JF03Z0NMXW0PXV\
    #     M86Z1&pd_rd_r=b592df2f-51e0-4fe5-8ccd-e6ff9930134e&pd_rd_wg=CLvfl&ref_=pd_gw_ci_mcx_mr_hp_d'

    product = Product(BASE_URL)

    DRIVER_PATH = os.path.abspath('drivers/chromedriver')
    # Set the driver options
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # linux only

    if args.raspi:
        print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Operação headless em raspberry pi')
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome(
            executable_path=DRIVER_PATH, options=chrome_options)

    driver.maximize_window()
    driver.implicitly_wait(10)
    print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Busca URL')
    driver.get(BASE_URL)
    print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} URL retornada')

    product.name = product.get_product_feature(
        driver, 'span', 'id', 'productTitle')
    product.price = product.get_product_feature(
        driver, 'span', 'id', 'priceblock_ourprice')

    if not product.name:
        print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Nome do produto não encontrado')
        # telegram_send.send(
        #     messages=["Ocorreu um erro ao buscar o produto, verificar no site"])
    else:
        print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Nome do produto encontrado com sucesso')

    if product.price:
        if product.name:
            print(f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Produto encontrado, enviando mensagem de alerta')
            telegram_send.send(messages=[
                f"Produto {product.name} encontrado por {product.price} na \
                url abaixo: \n\n {product.url}"])
        else:
            print(
                f'{datetime.now().strftime(' % d/%m/%Y % H: % M: % S')} Valor de produto encontrado, erro na busca pelo nome')
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
