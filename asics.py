import os
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
#import pandas as pd

#Prodotto, taglia e prezzo desiderato
search_term = 'kayano'
size = '42.5'
target_price = 127
url = f'https://outlet.asics.com/it/it-it/search/uomo/?q={search_term}&prefn1=sizeEU&prefv1={size}'

#Dati bot telegram
token = os.environ['TOKEN']
chat_id = '@lenovoscraper'

def getData(url):
  s = HTMLSession()
  r = s.get(url)
  r.html.render(sleep=1, timeout = 100)
  soup = BeautifulSoup(r.html.html, 'html.parser')
  return soup

def getProducts(soup):
  products_list = []
  #results = soup.find(id='search-result-items')
  products = soup.find_all('a', {'class': 'product-tile__link js-product-tile'})
  for item in products:
    url = item['href']
    title = item['title'].strip()
    prod_id = item['data-productid']
    #img = item.find('img')['src']
    price = item.find('span', {'class': 'price-sales price-sales-discount'}).text.replace("Prezzo di vendita","").replace(",",".").replace(" €","").strip()

    saleitem = {
      'prod_id': prod_id,
      'url': url,
      'title': title,
      #'img': img,
      'price': float(price)
    }

    products_list.append(saleitem)
  return products_list

def productFilter(list):
  wrong_prod = ['OBI','OG']
  res = [p for p in list if not any(w in p['title'] for w in wrong_prod)]
  return res

def send_telegram_messages(message,token,chat_id):
  request_url = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text=" + message
  requests.get(request_url)

#Main
s = getData(url) 
prod = getProducts(s)
res = productFilter(prod)
print(len(res))

for p in res:
  if p['price'] < target_price:
    msg =  f'{p["title"]} disponibile a {p["price"]}€\n{p["url"]}'
    send_telegram_messages(msg,token,chat_id)

#df = pd.DataFrame(products_list)
#print(df.head())
