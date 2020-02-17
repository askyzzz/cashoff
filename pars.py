import requests
from bs4 import BeautifulSoup
import lxml

user = input("Введите login: ")
password = input("Введите пароль: ")
base_url = 'https://fix-price.ru/personal/#profile'
action_url = 'https://fix-price.ru/actions/'
file_name = f"{user}__ParsingData.txt"

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

def url_get(base_url, file_name):
    session = url_auth(user, password)
    request = session.get(base_url)
    soup = BeautifulSoup(request.content, 'lxml')
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
#Избранное
    all_favorites = []
    favorites = soup.find_all('div', attrs={"class": "main-list__card-item"})
    for product in favorites:
        product_name = product.find("a", attrs={"class": "product-card__title"}).text
        product_name_strip= product_name.strip()
        product_name_just = product_name_strip.ljust(50, " ")
        price = product.find("span", attrs={"itemprop": "price"}).text
        all_favorites.append({
            "product_name": product_name_just,
            "price": price
        })
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"Фамилия: {last_name}\n")
        file.write(f"Имя: {name}\n")
        file.write(f"Отчество: {second_name}\n")
        file.write(f"EMAIL: {email}\n")
        file.write(f"Дата рождения: {personal_birthday}\n")
        file.write(f"Пол: {personal_gender}\n")
        file.write(f"Город: {personal_city}\n")
        file.write(f"Почтовый индекс: {personal_zip}\n")
        file.write(f"Номер карты: {personal_card_number}\n")
        file.write("\n")
        file.write("Избранное:\n")
        for item in all_favorites:
            file.write(f"Товар: {item['product_name']} Цена: {item['price']} руб.\n")
        file.write("\n")
#Акции
def url_action(action_url,file_name):
    session = url_auth(user, password)
    action = session.get(action_url)
    soup = BeautifulSoup(action.content, 'lxml')
    action_url = []
    try:
        pagination = soup.find_all("li", attrs={"class": "paging__item"})
        last_page = int(pagination[-1].text)
        for page in range(1, last_page +1):
            newPage = f'https://fix-price.ru/actions/?PAGEN_2={page}'
            action_page = session.get(newPage)
            soup = BeautifulSoup(action_page.content, 'lxml')
            items = soup.find_all("a", attrs={"class": "action-block__item"})
            for item in items:
                date = soup.find("div", attrs={"class": "action-card__date"}).text
                if not "акция завершена" in date:
                    title = item.find("h4", attrs={"class": "action-card__info"}).text
                    title = title.strip()
                    title = title.ljust(100, " ")
                    href = item['href']
                    action_url.append({
                        "Action": title,
                        "Url": f"https://fix-price.ru{href}"
                    })
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write("Акции:\n")
            for item in action_url:
                file.write(f"Акция: {item['Action']} Ссылка: {item['Url']}\n")
    except:
        pass
if __name__=='__main__':
    url_get(base_url, file_name)
    url_action(action_url, file_name)