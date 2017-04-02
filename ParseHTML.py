from bs4 import BeautifulSoup
import requests
import csv
import re

def GetFirmEMail(firm_site):
    # получаем главную страницу
    # ищем на ней почту
    # если не находим, ищем ссылку контакты

    main_page_firm = requests.get(firm_site).text
    soup = BeautifulSoup(page_firm, "html.parser")
    re.findall("/.+@.+\..+/i",main_page_firm)

    return ""

output_file = open("lifts.csv", "wb")
csv_out = csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
# page = requests.get('https://moscowinfo24.ru/prodazha-i-obsluzhivanie-liftov-v-moskve/').text
page = open('c:\\downloads\\lifts2.htm', encoding='utf-8').read()
document = BeautifulSoup(page, "html.parser")

firm_list_lxml = document.findAll('h4',{'class' : 'job-title'})
for item_lxml in firm_list_lxml:
    firm_name = item_lxml.find('a').text
    firm_link = item_lxml.find('a').get('href')

    # print('%s' % firm_name)

    firm_address = ""
    firm_phones = ""
    firm_site = ""
    firm_email = ""
    # парсим карточку фирмы
    page_firm = requests.get(firm_link).text
    soup = BeautifulSoup(page_firm, "html.parser")
    firm_cart_li = soup.find('ul', {'class': 'list-border'})
    for i in firm_cart_li.findAll('li'):
        i_text = i.text.strip()
        # нужно только первое двоеточие, останые должны остаться в val
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

    if (firm_email == "") and (firm_site != ""):
        firm_email = GetFirmEMail(firm_site)
    # csv_out.writerow([firm_name.encode('utf-8'), firm_address.encode("utf-8"), firm_phones.encode("utf-8"),
    #                   firm_site.encode("utf-8"), firm_email.encode("utf-8")])
    print("%s\t%s\t%s\t%s\t%s"%(firm_name,firm_address,firm_phones,firm_site,firm_email))

