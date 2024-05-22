import requests
from lxml import etree
from bs4 import BeautifulSoup


url = "https://bbr.ru"
response = requests.get(url)

if response.status_code == 200:
    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Преобразуем BeautifulSoup объект в объект lxml для использования XPath
    root = etree.HTML(str(soup))

    # Используем XPath для извлечения курса покупки йен
    result = root.xpath('//*[@id="__next"]/div/main/div/div[3]/div/div[2]/div[4]/div[2]/div[1]/span[1]/text()')

    if result:
        print("Курс покупки йен:", result[0])
    else:
        print("Не удалось найти курс покупки йен на странице.")
else:
    print("Ошибка при получении страницы. Код состояния:", response.status_code)



