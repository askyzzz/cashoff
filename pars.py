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
    print(name)

#url_auth(user, password)
#personal_data()
url_get(base_url)