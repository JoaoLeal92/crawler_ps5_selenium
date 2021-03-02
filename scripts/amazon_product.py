from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

class Product:
    def __init__(self, product_url):
        self.url = product_url
        self.name = None
        self.price = None
    
    def get_product_feature(self, driver, tag, tag_attr, tag_attr_value):
        try:
            product_feat_element = driver.find_element_by_xpath(f'//{tag}[@{tag_attr}="{tag_attr_value}"]')
            product_feat = product_feat_element.text
        except NoSuchElementException:
            return None
        except Exception as e:
            # Enviar mensagem de alerta telegram contendo a descrição do erro
            print(f'Ocorreu o seguinte erro: {e}')

        return product_feat
    