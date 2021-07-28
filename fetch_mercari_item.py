import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
import time
import re
from searched_item import *

HEADERS =  {"Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36}"}
MERCARI_BASE_URL = "https://www.mercari.com"
MERCARI_ITEM_URL = "https://www.mercari.com/jp/items/"
MERCARI_SEARCH_URL = MERCARI_BASE_URL + "/jp/search/"
        
class FetchMercariItem():
    
    @staticmethod
    def fetch_html(url:str) -> str:
        '''
        指定したurlのhtmlテキストを取得
        '''
        headers = HEADERS
        res = requests.get(url,headers=headers)
        if not(300 > res.status_code >= 200):
             raise Exception(f"リクエストエラー:{url} / status:{res.status_code}")
         
        return res.text 
    
    @staticmethod
    def fetch_mercari_items(urls:list):
        item_ids = []
        for url in urls:
            m = re.search(r"/items/(m[0-9]*)", url)
            if m == None:
                continue
            item_ids.append(m.group(1))
        items = []
        for id in item_ids:
            items.append(FetchMercariItem.fetch_mercari_item(MERCARI_ITEM_URL + id, id))
            time.sleep(3)
            
        return list(filter(None, items)) # Noneは除外
        
    @staticmethod
    def fetch_mercari_item(url:str, item_id:str):
        try:
            res_text = FetchMercariItem.fetch_html(url)
            soup = bs(res_text,"html.parser")
            
            item_id = item_id
            item_name = soup.select_one(".item-name")
            description = soup.select_one(".item-description-inner")
            table_th = soup.select(".item-detail-table th")
            table_td = soup.select(".item-detail-table td")
            images = soup.select(".luminous-gallery img")
            price = soup.select_one(".item-price")
            category_soup = FetchMercariItem.find_table_th_get_td(table_th, table_td, "カテゴリー",is_return_soup=True)
            category_soup = category_soup.select("div")
            brand = FetchMercariItem.find_table_th_get_td(table_th, table_td, "ブランド") 
            condition = FetchMercariItem.find_table_th_get_td(table_th, table_td, "商品の状態")
            shipping_payment = FetchMercariItem.find_table_th_get_td(table_th, table_td, "配送料の負担")
            shipping_method = FetchMercariItem.find_table_th_get_td(table_th, table_td, "配送の方法")
            shipping_prefecture = FetchMercariItem.find_table_th_get_td(table_th, table_td, "配送元地域")
            shipping_leadtime = FetchMercariItem.find_table_th_get_td(table_th, table_td, "発送日の目安")
            seller_name_soup =  FetchMercariItem.find_table_th_get_td(table_th, table_td, "出品者",is_return_soup=True)
            seller_name = seller_name_soup.select_one("a").text
        except Exception as e:
            print(e)
            return None

        thumbnail_url = images[0].get("data-src") if len(images) != 0 else None
        image_urls = [image.get("data-src") for image in images]
        price = price.text.replace("¥","").replace(",","")
        categories = [category.text for category in category_soup]
        
        return SearchedItem(item_name=item_name.text, item_id=item_id, description=description.text, 
                           thumbnail_url=thumbnail_url, image_urls=image_urls, categories=categories, brand=brand, condition=condition,
                           shipping_payment=shipping_payment, shipping_method=shipping_method, 
                           shipping_prefecture=shipping_prefecture, shipping_leadtime=shipping_leadtime,
                           seller_name=seller_name, site="mercari", url=url, price=int(price))
    
    @staticmethod
    def fetch_keyword_searched_item_urls(url:str):
        res_text = FetchMercariItem.fetch_html(url)
        soup = bs(res_text,"html.parser")
        items = soup.select(".items-box a")
        item_urls = [item.get("href") for item in items]
        
        return item_urls
    
    @staticmethod
    def fetch_keyword_searched_items(keyword:str, min_price:int=0, max_price:int=None):
        url = MERCARI_SEARCH_URL + "?" + FetchMercariItem.create_search_query(keyword,min_price,max_price)
        urls = FetchMercariItem.fetch_keyword_searched_item_urls(url)
        items = []
        for url in urls:
            item = FetchMercariItem.fetch_mercari_item(MERCARI_BASE_URL + url)
            if item != None:
                items.append(item)

        return items
    
    @staticmethod
    def create_search_query(keyword:str, min_price:int=0, max_price:int=None):
        query_dict = {
            "keyword":keyword,
            "price_min":min_price,
            "price_max":max_price,
            "item_condition_id[1]":1,
            "status_on_sale":1,
            "sort_order":"",
            "category_root":"",
            "brand_name":"",
            "brand_id":"",
            "size_group":""
        }
        return urlencode(query_dict)
    
    @staticmethod
    def find_table_th_get_td(th_list,td_list, target:str, is_return_soup:bool=False):
        for th,td in zip(th_list,td_list):
            if th.text == target:
                if is_return_soup:
                    return td
                else:
                    return td.text
        else:
            return None