class SearchedItem():
    
    def __init__(self, 
                 item_name:str, description:str, item_id:str, image_urls:list, thumbnail_url:str, categories:list, 
                 brand:str, condition:str, shipping_payment:str, shipping_method:str,
                 shipping_prefecture:str, shipping_leadtime:str, seller_name:str, site:str, url:str, price:int):
        self.item_name = item_name
        self.description = description
        self.item_id = item_id
        self.image_urls = image_urls
        self.thumbnail_url = thumbnail_url
        self.categories = categories
        self.brand = brand
        self.condition = condition
        self.shipping_payment = shipping_payment
        self.shipping_method = shipping_method
        self.shipping_prefecture = shipping_prefecture
        self.shipping_leadtime = shipping_leadtime
        self.seller_name = seller_name
        self.is_remove = False
        self.site = site
        self.url = url
        self.price = price
        self.amazon_price = 0
        