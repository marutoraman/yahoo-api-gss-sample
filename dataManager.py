import dataclasses

CATEGORY_LIST = ["選択してください", "レディース", "メンズ", "ベビー・キッズ", "インテリア・住まい・小物", "本・音楽・ゲーム", "おもちゃ・ホビー・グッズ", "コスメ・香水・美容", "家電・スマホ・カメラ",  "スポーツ・レジャー", "ハンドメイド", "チケット", "自動車・オートバイ", "その他"]
ITEM_STATUS =["選択してください", "新品、未使用", "未使用に近い", "目立った傷や汚れなし", "やや傷や汚れあり", "傷や汚れあり", "全体的に状態が悪い"]
RECEIVE = ["選択してください", "送料込み(出品者負担)", "着払い(購入者負担)"]
FROM_AREA = ["選択してください", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県", "未定"]
SHIPMENT = ["選択してください", "1〜2日で発送", "2〜3日で発送", "4〜7日で発送"]

@dataclasses.dataclass
class Item_Info:
    image_file_name: str
    title: str
    detail: str
    category: str
    brand: str
    status: int
    price: int
    discount_rate: float
    
@dataclasses.dataclass
class Delivery_Info:
    payer: int
    send_from: int
    shipment_period: int

def get_item_info(datum):
    image_file_name = datum[0]
    title = datum[1]
    detail = datum[2]
    category = datum[3]
    brand = datum[4]
    status = datum[5]
    price = datum[6]
    item_info = Item_Info(image_file_name, title, detail, category, brand, status, price)
    return item_info

def get_delivery_info(datum):
    payer = datum[10]
    send_from = datum[11]
    shipment_period = datum[12]
    delivery_info = Delivery_Info(payer, send_from, shipment_period)
    return delivery_info

def get_price(datum):
    price = datum[]
    discount_rate = datum[]
    return price * discount_rate