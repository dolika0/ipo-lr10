from bs4 import BeautifulSoup
import requests

url = "https://quotes.toscrape.com/"

page = requests.get(url) #  Отправим GET()-запрос на сайт
print(page.status_code) # Проверяем подключение к сайту

# if page != 200:
#     print(f"ошибка при запросе на сайт {page}")
#     exit() # Выход из текущего программного блока

soup = BeautifulSoup(page.text, "html.parser") 
print(soup) # Покажет весь код страницы

allQuote = soup.findAll('div', class_='quote') # Находим все цитаты
print(allQuote)

print("Найдено цитат: ", len(allQuote))

titles = [] # авторы
comments = [] # цитаты

for quote in allQuote:
    if quote.find('span', class_='author') is not None:
        titles.append(quote.text)

print(titles)
