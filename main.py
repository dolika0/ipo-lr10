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

# Находим все цитаты
quote_elements = soup.find_all('div', class_='quote')

# Отладочные сообщения для проверки получения данных
print(f"Найдено цитат: {len(quote_elements)}")

# Списки для цитат и авторов
list_quotes = []
list_authors = []

# Заполняем списки данными
for quote in quote_elements:
    text = quote.select_one('.text').get_text(strip=True)
    author = quote.select_one('.author').get_text(strip=True)
    list_quotes.append(text)
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
with open(file_json, "w", encoding='utf-8') as file:
    json.dump(writer_list, file, indent=4, ensure_ascii=False)

print("Проверяем содержимое файла data.json:")
with open(file_json, "r", encoding='utf-8') as file:
    data = json.load(file)
    print(json.dumps(data, indent=4, ensure_ascii=False))

# Генерация HTML файла на основе данных из data.json
file_index = "index.html"

with open(file_index, "w", encoding='utf-8') as file:
    file.write("""<html>
<head>
    <title>Quotes to Scrape</title>
    <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            background-color: #fff;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
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
    <p style="text-align: center;"><a href="http://quotes.toscrape.com/">Источник данных</a></p>
</body>
</html>
""")

print("HTML файл создан: index.html")
