import lxml.html
from bs4 import BeautifulSoup
import requests
import csv

output_file = open("lifts.csv", "wb")
csv_out = csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
# page = requests.get('https://moscowinfo24.ru/prodazha-i-obsluzhivanie-liftov-v-moskve/').text
page = open('c:\\downloads\\lifts2.htm', encoding='utf-8').read()
document = lxml.html.fromstring(page)

# firm_list_lxml = document.xpath('//a[@class = "title"]')
firm_list_lxml = document.xpath('//h4[@class = "job-title"]/a')
for item_lxml in firm_list_lxml:
    firm_name = item_lxml.xpath('text()')[0]
    firm_link = item_lxml.xpath('@href')[0]
    firm_name = str(firm_name)
    print('%s' % firm_name)

    firm_address = ""
    firm_phones = ""
    firm_site = ""
    firm_email = ""
    # парсим карточку фирмы
    page_firm = requests.get(firm_link).text
    soup = BeautifulSoup(page_firm, "lxml")
    # firm_cart_soup = soup.find('div', {'class': 'org-Details'})
    # firm_cart_address = soup.find('ul', {'class': 'list-border'}).find('li').text
    firm_cart_li = soup.find('ul', {'class': 'list-border'})
    for i in firm_cart_li.findAll('li'):
        # print(i.text)
        i_text = i.text.strip()
        pos = i_text.find(":")
        par = str(i_text[:pos])
        val = str(i_text[pos:])
        if par == "Адрес":
            firm_address = val
        elif par == "Телефон":
            firm_phones = firm_phones + val + " "
        elif par == "Сайт":
            firm_site = val
        elif par == "Email":
            firm_email = val

    # document_firm = lxml.html.fromstring(page_firm)
    # firm_cart_lxml = document.xpath('//div[@class = "org-Details"]')
    # for i in firm_cart_lxml:
    #     print(i.xpath('/li/text()')[0])

    s1 = firm_name.encode('utf-8')
    print(type(s1))
    csv_out.writerow([s1])
    # csv_out.writerow([firm_name.encode('utf-8'), firm_address."utf-8"), bytes(firm_phones,"utf-8"),
    #                   bytes(firm_site,"utf-8"), bytes(firm_email,"utf-8")])

csv_out.close()
