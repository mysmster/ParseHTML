import lxml.html
from bs4 import BeautifulSoup
import requests

# page = requests.get('https://moscowinfo24.ru/prodazha-i-obsluzhivanie-liftov-v-moskve/').text
page = open('c:\\downloads\\lifts2.htm', encoding='utf-8').read()
document = lxml.html.fromstring(page)

# firm_list_lxml = document.xpath('//a[@class = "title"]')
firm_list_lxml = document.xpath('//h4[@class = "job-title"]/a')
for item_lxml in firm_list_lxml:
    firm_name = item_lxml.xpath('text()')[0]
    firm_link = item_lxml.xpath('@href')[0]
    print('%s %s' % (firm_name, firm_link))

    # парсим карточку фирмы
    page_firm = requests.get(firm_link).text
    soup = BeautifulSoup(page_firm)
    firm_cart_soup = soup.find('div', {'class': 'org-Details'})
    firm_cart_address = soup.find('ul', {'class': 'list-border'}).find('li').text
    firm_cart_li = soup.find('ul', {'class': 'list-border'})
    for i in firm_cart_li.findAll('li'):
        print(i)

    # document_firm = lxml.html.fromstring(page_firm)
    # firm_cart_lxml = document.xpath('//div[@class = "org-Details"]')
    # for i in firm_cart_lxml:
    #     print(i.xpath('/li/text()')[0])
