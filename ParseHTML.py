from bs4 import BeautifulSoup
import requests
import csv
import re

def GetFirmEMail(firm_site):
    # получаем главную страницу
    # ищем на ней почту
    # если не находим, ищем ссылку контакты

    str_mails = ""

    try:
        main_page_firm = requests.get(firm_site).text
    except:
        return str_mails

    # очистка от тегов для удобства поиска и возможных тего внутри почты
    p = re.compile(r'<.*?>')
    main_page_firm_text = p.sub('', main_page_firm)
    # поиск почтового адреса
    p = re.compile(r"([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}", re.MULTILINE)
    mail_mail = p.finditer(main_page_firm_text)
    if mail_mail:
        # адрес есть на главной странице
        str_mails = ",".join([m.group() for m in mail_mail])
    if str_mails == "":
        # надо искать адрес в контактах
        # контактная
        p = re.compile(r"(Контакты|Контактная информация)", re.MULTILINE)
        mail_mail = p.finditer(main_page_firm)
        for m in mail_mail:
            #print (m.span())
            m_block = main_page_firm[m.span()[0] - 64:m.span()[0]]
            #print(m_block)
            lst_href = re.findall(r'href="(.*)"', m_block)
            if lst_href:
                if firm_site[-1] != '/':
                    firm_site = firm_site + '/'
                str_href = lst_href[0] if not '"' in lst_href[0] else lst_href[0][:lst_href[0].find('"')]
                if str_href not in firm_site:
                    str_cont_ref = firm_site+str_href if not ":" in str_href else str_href
                    str_mails = str_mails + " " + GetFirmEMail(str_cont_ref)
    return str_mails

output_file = open("lifts.csv", "wb")
csv_out = csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
# page = requests.get('https://moscowinfo24.ru/prodazha-i-obsluzhivanie-liftov-v-moskve/').text
page = open('lifts2.htm', encoding='utf-8').read()
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
        par = str(i_text[:pos]).strip()
        val = str(i_text[pos+1:]).strip()
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

