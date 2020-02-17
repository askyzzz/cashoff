import requests
from bs4 import BeautifulSoup
import logging

user = 'aleksandra.grinina@mail.ru'
password = 'Fixprice123'
base_url = 'https://fix-price.ru/personal/#profile'

def url_auth(user, password):
    session = requests.Session()
    request_auth = session.post('https://fix-price.ru/ajax/auth_user.php', {
        "AUTH_FORM": "Y",
        "TYPE": "AUTH",
        "backurl": "/personal/",
        "login": f'{user}',
        "password": f'{password}'
    })
    if request_auth.json()['res'] == 1:
        print("Auth is ok")
        return session
    else:
        print("error auth")
        return exit(1)

def url_get(base_url):
    session = url_auth(user, password)
    request = session.get(base_url)
    soup = BeautifulSoup(request.content, 'html.parser')
    name = soup.find("input", attrs={"name": "NAME"})['value']
    last_name = soup.find("input", attrs={"name": "LAST_NAME"})['value']
    second_name = soup.find("input", attrs={"name": "SECOND_NAME"})['value']
    email = soup.find("input", attrs={"placeholder": "*EMAIL"})['value']
    personal_birthday = soup.find("input", attrs={"name": "PERSONAL_BIRTHDAY"})['value']
    personal_gender_check = soup.find("input", attrs={"checked": "checked"})['value']
    if personal_gender_check == "F":
        personal_gender = "Женский"
    else:
        personal_gender = "Мужской"
    personal_zip = soup.find("input", attrs={"name": "PERSONAL_ZIP"})['value']
    personal_city = soup.find("select", attrs={"name": "PERSONAL_CITY"})['data-value']
    personal_card_number = soup.find("div", attrs={"class": "personal-card__number"}).text
#    return name, second_name, last_name, email, personal_birthday, personal_gender, personal_city, personal_zip, personal_card_number

    all_favorites = []
    favorites = soup.find_all('div', attrs={"class": "main-list__card-item"})
    for product in favorites:
        product_name = product.find("a", attrs={"class": "product-card__title"}).text
        product_name_strip= product_name.strip()
        price = product.find("span", attrs={"itemprop": "price"}).text
        all_favorites.append({
            "product_name": product_name_strip,
            "price": price
        })
#        print(product_name)

    with open('pesonal_data.txt', 'w', encoding='utf-8') as file:
        file.write(f"Фамилия: {last_name}\n")
        file.write(f"Имя: {name}\n")
        file.write(f"Отчество: {second_name}\n")
        file.write(f"Дата рождения: {personal_birthday}\n")
        file.write(f"Пол: {personal_gender}\n")
        file.write(f"Город: {personal_city}\n")
        file.write(f"Почтовый индекс: {personal_zip}\n")
        file.write(f"Номер карты: {personal_card_number}\n")
        file.write("Избранное\n")
        for item in all_favorites:
            file.write(f"Товар: {item['product_name']} Цена: {item['price']}\n")


#url_auth(user, password)
#personal_data()
url_get(base_url)