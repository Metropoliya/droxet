import requests
from bs4 import BeautifulSoup
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProductAvailabilityScraper:
    def __init__(self, url, user_agent):
        self.url = url
        self.headers = {
            'User-Agent': user_agent
        }

    def fetch_page(self):
        """
        Выполняет HTTP-запрос к указанному URL и возвращает HTML-контент страницы.
        В случае ошибки выбрасывает исключение.
        """
        try:
            logging.info(f"Fetching page: {self.url}")
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Если код ответа не 200, выбросить ошибку
            return response.text
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Error connecting to {self.url}: {conn_err}")
            raise
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error: {timeout_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred: {req_err}")
            raise

    def parse_availability(self, html):
        """
        Парсит HTML страницы и ищет наличие товара по классу "l-icon-box__content".
        Возвращает текст с информацией о наличии товара или None, если не найдено.
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Ищем элемент <span> с классом "l-icon-box__content"
        availability_tag = soup.find('span', class_='c-product-available c-product-available_out-of-stock c-product-available_size_s')
        if availability_tag:
            availability_text = availability_tag.text.strip()
            logging.info(f"Found availability text: {availability_text}")
            return availability_text
        else:
            logging.warning("Availability tag not found.")
            return None

    def check_availability(self):
        """
        Основной метод, который выполняет запрос страницы и парсит информацию о наличии товара.
        Возвращает структуру данных с информацией о наличии или сообщает об отсутствии данных.
        """
        try:
            html = self.fetch_page()
            availability_text = self.parse_availability(html)
            
            # Проверяем, есть ли текст "Нет в наличии"
            if availability_text == "Нет в наличии":
                return {"status": "out_of_stock", "message": "Product is not available"}
            elif availability_text:
                return {"status": "in_stock", "message": f"Product availability: {availability_text}"}
            else:
                return {"status": "unknown", "message": "Availability information not found"}
        
        except Exception as e:
            logging.error(f"Failed to check product availability: {e}")
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # URL страницы и User-Agent браузера
    url = "https://xn--51-6kcd9bfu4aij.xn--p1ai/tolstovka-teriberka-kit-severnoe-siyanie/"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    # Инициализация скраппера и проверка наличия товара
    scraper = ProductAvailabilityScraper(url, user_agent)
    result = scraper.check_availability()
    
    # Логируем результат
    logging.info(f"Availability Check Result: {result}")
