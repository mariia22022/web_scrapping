import requests
import bs4
import re
import lxml

# ключевые слова поиска
KEYWORDS = ['гайд', 'дизайн', 'уязвимост']

# регулярное выражения для поиска по ключевым словам
pattern = fr'({KEYWORDS[0]}[а-я]+|{KEYWORDS[1]}[а-я]+|{KEYWORDS[2]}[а-я]+)'

response = requests.get('https://habr.com/ru/articles/')
soup = bs4.BeautifulSoup(response.text, features='lxml')

all_articles = soup.findAll('h2', class_='tm-title tm-title_h2')

articles_list = []
#  собираем все ссылки на статьи в один список
for art in all_articles:
    link = f"https://habr.com{art.find('a', class_='tm-title__link')['href']}"

    response_link = requests.get(link)
    soup_link = bs4.BeautifulSoup(response_link.text, features='lxml')

    title = soup_link.find('h1').text.strip()
    time = soup_link.find('time')['datetime']
    text = soup_link.find_all('p')

    # ищем ключевые слова в заголовке и тексте статьи
    result = re.findall(pattern, title, re.IGNORECASE)
    result2 = re.findall(pattern, str(text), re.IGNORECASE)
    if result or result2:
        articles_list.append({'time': time, 'title': title, 'link': link})

for article in articles_list:
    print(*article.values(), sep='   -   ')
