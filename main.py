import requests
from bs4 import BeautifulSoup

# ----------------------------av.by------------------------------

# headers = {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
# #
# params = {"page":"29"}
# url = 'https://cars.av.by/filter'
# req = requests.get(url, headers=headers, params=params)
# print(req.text)


# -----------------------faber-------------------------------------------------
idies_category = {"Уход": "1001159186333",
                  "Макияж": "1001159186332",
                  "Парфюмерия": "1000175334690",
                  "Мода": "1000175334844",
                  "Здоровье": "1000175334795",
                  "BIOSEA": "1001137423362",
                  "Дом": "1000175334776",
                  "Бизнес": "1000180022575",
                  }


#
# headers = {
#     "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
#
# params = {"option": "com_catalog",
#           "view": "listgoods",
#           "idcategory": "1000175334776",
#           "Itemid": "2075",
#           "lang": "ru"
#           }
#
# params_actions = {
#     "option": "com_catalog",
#     "view": "listgoods",
#     "bpromo": "1",
#     "Itemid": "2075",
#     "lang": "ru"
#
# }
#
# url = "https://faberlic.com/index.php"
#
# req = requests.get(url, headers=headers, params=params)
#
# print(req.text)


class Page():
    url = "https://faberlic.com/index.php"
    params_actions = {
        "option": "com_catalog",
        "view": "listgoods",
        "bpromo": "1",
        "Itemid": "2075",
        "lang": "ru"
    }

    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    def __init__(self):
        self.params = {"option": "com_catalog",
                  "view": "listgoods",
                  "idcategory": "1000175334776",
                  "Itemid": "2075",
                  "lang": "ru"
                  }

    def choise_id(self, id):
        self.params["idcategory"] = f"{id}"

    def get_page(self):
        params = self.params
        req = requests.get(Page.url, headers=Page.headers, params=params).text
        return req


class List_Products():
    def __init__(self):
        self.page = Page

    def get_list_products(self):
        a = self.page.get_page()
        soup = BeautifulSoup(a, 'html.parser')
        list_products = soup.find_all('a', class_='card')
        for a in list_products:
            prod = Product()
            prod.get_product(a)


class Product():
    def __init__(self):
        self.name = ''
        self.href = ''
        self.id = ''
        self.price = ''
        self.nal = ''
        self.image = ''

    def get_product(self, a):
        self.name = a.find('img').attrs["alt"]
        self.href = 'https://faberlic.com/' + a.attrs["href"]
        self.id = a.find(class_="cardImg").attrs["rel"].replace('{', '').replace('}', '').replace('"', '').split(":")[1]
        self.price = float(a.find(class_="cardPrice cardPriceSale cardPriceSaleRed").text.replace('BYN', ''))
        self.nal = a.find(class_="add_to_cart").text
        if self.nal == "Добавить":
            self.nal = 'Имеется в наличии'
        self.image = a.find('img').attrs['firstimage']

        print(f'Наименование: {self.name}\n'
              f'Ссылка:  {self.href}\n'
              f'Цена: {self.price} BYN\n'
              f'Наличие: {self.nal}\n\n')


page = Page()
# list_prod = List_Products()
# list_prod.get_list_products()
for id in idies_category.values():
    page.choise_id(id)
    page.get_page()
    list_prod = List_Products()
    list_prod.get_list_products()
