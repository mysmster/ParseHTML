import lxml.html
import requests

#page = requests.get('https://moscowinfo24.ru/prodazha-i-obsluzhivanie-liftov-v-moskve/').text
page = open('c:\\downloads\\lifts.htm',encoding='utf-8').read()
document = lxml.html.fromstring(page)

firm_list_lxml = document.xpath('//a[@class = "title"]')
for item_lxml in firm_list_lxml:
    firm_name = item_lxml.xpath('text()')[0]
    firm_link =  item_lxml.xpath('@href')[0]
    print ('%s %s'%(firm_name,firm_link))

    # парсим карточку фирмы
    page_firm = requests.get(firm_link).text
    document_firm = lxml.html.fromstring(page)
    #firm_cart_lxml = document.xpath('//ul[@class = "listoption"]')
    firm_cart_lxml = document.xpath('//div[@class = "container"]')
    for i in firm_cart_lxml:
        print(i.xpath('div')[0])
