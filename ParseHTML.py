import lxml.html
import requests

#page = requests.get('https://moscowinfo24.ru/prodazha-i-obsluzhivanie-liftov-v-moskve/').text
page = open('c:\\downloads\\lifts2.htm',encoding='utf-8').read()
document = lxml.html.fromstring(page)

#firm_list_lxml = document.xpath('//a[@class = "title"]')
firm_list_lxml = document.xpath('//h4[@class = "job-title"]/a')
for item_lxml in firm_list_lxml:
    firm_name = item_lxml.xpath('text()')[0]
    firm_link =  item_lxml.xpath('@href')[0]
    print ('%s %s'%(firm_name,firm_link))

    # парсим карточку фирмы
    document_firm = lxml.html.fromstring(page)
    page_firm = requests.get(firm_link).text
    firm_cart_lxml = document.xpath('//div[@class = "col-sm-8"]')
    for i in firm_cart_lxml:
        print(i.xpath('/li/text()')[0])