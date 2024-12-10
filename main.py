import requests
from bs4 import BeautifulSoup
import json

# URL для парсинга
url = 'http://quotes.toscrape.com/'

# Отправляем GET-запрос
response = requests.get(url)
if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Находим все цитаты по классу
quote_elements = soup.find_all('div', class_ = 'quote')

# Выводим кол-во найденных цитат
print(f"Найдено цитат: {len(quote_elements)}")

# Списки для цитат и авторов
list_quotes = []
list_authors = []

# Заполняем списки данными
for quote in quote_elements:

    text = quote.select_one('.text').get_text(strip = True)
    list_quotes.append(text)

    author = quote.select_one('.author').get_text(strip = True)
    list_authors.append(author)

# Выводим данные в требуемом формате
for i in range(len(list_quotes)):
    print(f"{i + 1}. Quote: {list_quotes[i]}; Author: {list_authors[i]};")

# Сохранение данных в файл data.json
file_json = "data.json"
writer_list = []

for i in range(len(list_quotes)):
    writer = {'Quote': list_quotes[i], 'Author': list_authors[i]}
    writer_list.append(writer)

print("Записываем данные в файл data.json")
with open(file_json, "w", encoding = 'utf-8') as file:
    json.dump(writer_list, file, indent = 4)

print("Проверяем содержимое файла data.json:")
with open(file_json, "r", encoding = 'utf-8') as file:
    data = json.load(file)
    print(json.dumps(data, indent = 4)) # Преобразуем обратно в json, с отступами в 4 пробела

# Генерация HTML файла на основе данных из data.json
file_index = "index.html"

with open(file_index, "w", encoding = 'utf-8') as file:
    file.write("""<html>
<head>
    <title>Quotes to Scrape</title>
    <style>
        body {
            background-color: #fde2ff;
            font-family: Cascadia Code SemiLight;
        }
        h1 {
            text-align: center;
            color: #9a18b0;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            background-color: #ffffff;
        }
        th, td {
            border: 1px solid #8a089c;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #fd9dad;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #ffffff;
        }
    </style>
</head>
<body>
    <h1>Quotes to Scrape</h1>
    <table>
        <tr>
            <th>Number</th>
            <th>Quote</th>
            <th>Author</th>
        </tr>
""")

    with open(file_json, "r", encoding='utf-8') as input_file:
        data_writer = json.load(input_file)
        for i, item in enumerate(data_writer):
            file.write(f"<tr><td>{i + 1}</td><td>{item['Quote']}</td><td>{item['Author']}</td></tr>\n")

    file.write("""
    </table>
    <p style="text-align: center;"><i><a href="http://quotes.toscrape.com/">Оригинальный источник данных</a></i></p>
</body>
</html>
""")

print("HTML файл создан: index.html")
