import requests
from bs4 import BeautifulSoup
import json
from bs4 import Tag

url = 'http://quotes.toscrape.com/'  # URL для парсинга

response = requests.get(url)  # Отправляем GET-запрос
if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

quote_elements = soup.find_all('div', class_='quote')  # Находим все цитаты по классу

print(f"Найдено цитат: {len(quote_elements)}")  # Выводим кол-во найденных цитат

list_quotes = []  # Списки для цитат
list_authors = []  # Списки для авторов

for quote in quote_elements:  # Заполняем списки данными
    text = quote.select_one('.text').get_text(strip=True)
    list_quotes.append(text)

    author = quote.select_one('.author').get_text(strip=True)
    list_authors.append(author)

for i in range(len(list_quotes)):  # Выводим данные в требуемом формате
    print(f"{i + 1}. Quote: {list_quotes[i]}; Author: {list_authors[i]};")

# Сохранение данных в файл data.json
file_json = "data.json"
writer_list = []

for i in range(len(list_quotes)):
    writer = {'Quote': list_quotes[i], 'Author': list_authors[i]}
    writer_list.append(writer)

print("Записываем данные в файл data.json")
with open(file_json, "w", encoding='utf-8') as file:
    json.dump(writer_list, file, indent=4)

print("Проверяем содержимое файла data.json:")
with open(file_json, "r", encoding='utf-8') as file:
    data = json.load(file)
    print(json.dumps(data, indent=4))  # Преобразуем обратно в json, с отступами в 4 пробела

def generate_html(data_file="data.json", template_file="template.html", output_file="index.html"):
    with open(data_file, "r", encoding="utf-8") as f:  # Загрузка данных из JSON
        quotes = json.load(f)

    with open(template_file, "r", encoding="utf-8") as f:  # Загрузка HTML-шаблона
        template = f.read()

    soup = BeautifulSoup(template, "html.parser")  # Парсинг шаблона

    container = soup.find("div", class_="place-here")  # Нахождение элемента для вставки таблицы
    if not container:
        raise ValueError("В шаблоне отсутствует элемент с классом 'place-here' для вставки таблицы.")

    table = Tag(name="table", attrs={"class": "quotes-table"})  # Создание таблицы

    # Создание заголовков таблицы
    thead = Tag(name="thead") 
    tr_head = Tag(name="tr")
    headers = ["№", "Quotes", "Author"]
    for header in headers:
        th = Tag(name="th")
        th.string = header
        tr_head.append(th)
    thead.append(tr_head)
    table.append(thead)

    # Создание строк таблицы
    tbody = Tag(name="tbody")
    for idx, quote in enumerate(quotes, start=1):
        tr = Tag(name="tr")

        td_num = Tag(name="td")
        td_num.string = str(idx)
        tr.append(td_num)

        td_quote = Tag(name="td")
        td_quote.string = quote["Quote"]
        tr.append(td_quote)

        td_author = Tag(name="td")
        td_author.string = quote["Author"]  
        tr.append(td_author)

        tbody.append(tr)
    table.append(tbody)

    # Вставка таблицы в шаблон
    container.append(table)

    # Сохранение результата в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())


generate_html()
print("HTML файл создан: index.html")
