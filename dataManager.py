import dataclasses
import spreadsheetManager

MAIN_CATEGORY_LIST = ["選択してください", "レディース", "メンズ", "ベビー・キッズ", "インテリア・住まい・小物", "本・音楽・ゲーム", "おもちゃ・ホビー・グッズ", "コスメ・香水・美容", "家電・スマホ・カメラ",  "スポーツ・レジャー", "ハンドメイド", "チケット", "自動車・オートバイ", "その他"]
SUB_CATEGORY_LIST = []
CATEGORY_DETAIL_LIST = []
ITEM_STATUS =["選択してください", "新品、未使用", "未使用に近い", "目立った傷や汚れなし", "やや傷や汚れあり", "傷や汚れあり", "全体的に状態が悪い"]
PAYMENT = ["選択してください", "送料込み(出品者負担)", "着払い(購入者負担)"]
FROM_AREA = ["選択してください", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県", "未定"]
SHIPMENT = ["選択してください", "1〜2日で発送", "2〜3日で発送", "4〜7日で発送"]

JSONKEY = 'testspreadsheet-302003-fb8fe37d15e6.json'
FILE = 'testspreadsheet'

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
@dataclasses.dataclass
class Item_Info:
    image_file_name: str
    title: str
    detail: str  ## detail_templateを用意必要
    main_category: int
    sub_category: int
    category_detail: int
    size: int
    brand: str # 非必須
    status: int 
    price: int
    discount_rate: float
    discount_limit: int
    
@dataclasses.dataclass
class Shipping_Info:
    payer: int
    method: int
    from_area: int
    duration: int

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def category_to_int(category):
    try:
        index = MAIN_CATEGORY_LIST.index(category)
        return index
    except ValueError as e:
        print(e)
    except:
        print("some thing went wrong converting [category] to int")

def status_to_int(status):
    try:
        index = ITEM_STATUS.index(status)
        return index
    except ValueError as e:
        print(e)
    except:
        print("some thing went wrong converting [status] to int")

def payment_to_int(payment):
    try:
        index = PAYMENT.index(payment)
        return index
    except ValueError as e:
        print(e)
    except:
        print("some thing went wrong converting [payment] to int")

def area_to_int(area):
    try:
        index = FROM_AREA.index(area)
        if area == "未定":
            index = 99
        return index
    except ValueError as e:
        print(e)
    except:
        print("some thing went wrong converting [area] to int")

def shipment_to_int(shipment):
    try:
        index = SHIPMENT.index(shipment)
        return index
    except ValueError as e:
        print(e)
    except:
        print("some thing went wrong converting [shipment] to int")

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

## 今回の肝！！！
def make_item_detail(datum):
    # template_type の変数を設定
    # type = datum[]
    # if type == 0:
    #     file = ""
    #     sheet_no = 0
    # elif type == 1:
    #     file = ""
    #     sheet_no = 0
    
    file = FILE
    sheet_no = 2

    # templateのDL
    template_sheet = spreadsheetManager.connect_to(JSONKEY, file, sheet_no)
    template = spreadsheetManager.fetch_allData(template_sheet)

    # DLしたtemplateから 使用されている $変数$ をlistで抽出


    # その$変数$に対する商品の値を取得

    # 取得した値を置換

    # detailに代入し、return
    detail = ""
    return detail

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def get_item_info(datum):
    image_file_name = datum[0]
    title = datum[1]
    detail_type = datum[2]
    detail = make_item_detail(datum)
    main_category = category_to_int(datum[4])
    sub_category = category_to_int(datum[4])
    category_detail = category_to_int(datum[4])
    size = datum[5]
    brand = datum[5]
    status = status_to_int(datum[6])
    price = datum[7]
    discount_rate = datum[8]
    discount_limit = datum[9]
    item_info = Item_Info(image_file_name, title, detail, main_category, sub_category, category_detail, size, brand, status, price, discount_rate, discount_limit)
    return item_info

def get_delivery_info(datum):
    payer = datum[10]
    method = datum[11]
    send_Area = datum[11]
    shipment_period = datum[12]
    delivery_info = Shipping_Info(payer, method, send_Area, shipment_period)
    return delivery_info

def get_price(datum):
    price = datum[14]
    discount_rate = datum[15]
    discount_limit = datum[16]
    calculated_price = price * discount_rate
    if calculated_price < discount_limit:
        calculated_price = discount_limit
    return calculated_price

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def get_dummy_item_info():
    item = Item_Info("002", "WALLY  シルバースタッズ", "商品詳細", 2, 4, 2, 8, "no brand", 1, 500000, 0.1, 450000)
    return item

def get_dummy_shippment_info():
    shipping_info = Shipping_Info(1, 2, 4, 1)
    return shipping_info

