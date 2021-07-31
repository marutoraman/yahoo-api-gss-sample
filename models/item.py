
class Item():

    def __init__(
        self, name: str, price: int, review_count: int, 
        review_average: float, url: str, jan: str):
        self.name = name
        self.price = price
        self.review_count = review_count
        self.review_average = review_average
        self.url = url
        self.jan = jan