import os, glob, time
import datetime as dt
from dataManager import Item_Info, Shipping_Info
import driverManager
from selenium.webdriver.support.select import Select

TOP = "https://www.mercari.com/jp/"
SELL_URL = "https://www.mercari.com/jp/sell"
SELLING_URL = "https://www.mercari.com/jp/mypage/listings/listing/"

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def start():
    global driver
    driver = driverManager.start_driver()
    driver = driverManager.open_page(driver, TOP)

def login():
    global driver
    driver.find_element_by_link_text("ログイン").click()

def close():
    global driver
    driverManager.close_driver(driver)
    driverManager.quit_driver(driver)

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def move_to_top():
    global driver
    driver = driverManager.open_page(driver, TOP)

def move_to_url(url: str):
    global driver
    driver = driverManager.open_page(driver, url)

def go_to_sell_page():
    global driver
    driver = driverManager.open_page(driver, SELL_URL)

def go_to_selling_page():
    global driver
    driver = driverManager.open_page(driver, SELLING_URL)

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def set_item(item_info: Item_Info):
    global driver
    # fileの中身を取得
    directory_path = os.getcwd()
    image_files = glob.glob(directory_path + '/002/*')
    # image: str
    for image in image_files:
        driver.find_element_by_xpath("//input[contains(@type, 'file') and contains(@accept, 'image/png,image/jpeg')]").send_keys(image)
    # title: str    
    driver.find_element_by_xpath("//input[contains(@type, 'text') and contains(@name, 'name')]").send_keys(item_info.title)
    # detail: str
    driver.find_element_by_xpath("//textarea[@name='description']").send_keys(item_info.detail)
    # main_category: int
    category_selector = driver.find_elements_by_xpath("//select[@name='categoryId']")
    main_category = Select(category_selector[0])
    main_category.select_by_index(item_info.main_category)
    # sub_category: int
    time.sleep(1)
    category_selector = driver.find_elements_by_xpath("//select[@name='categoryId']")
    sub_category = Select(category_selector[1])
    sub_category.select_by_index(item_info.sub_category)
    # category_detail: int
    time.sleep(1)
    category_selector = driver.find_elements_by_xpath("//select[@name='categoryId']")
    category_detail = Select(category_selector[2])
    category_detail.select_by_index(item_info.category_detail)
    # size: int
    size_selector = driver.find_element_by_xpath("//select[@name='size']")
    size = Select(size_selector)
    size.select_by_index(item_info.size)
    # brand: str 非必須
    driver.find_element_by_xpath("//input[contains(@type, 'text') and contains(@name, 'brandName')]").send_keys(item_info.brand)
    # status: int
    status_selector = driver.find_element_by_xpath("//select[@name='itemCondition']")
    status = Select(status_selector)
    status.select_by_index(item_info.status)

def set_delivery(shipping_info: Shipping_Info):
    global driver
    # payer: int
    payer_selector = driver.find_element_by_xpath("//select[@name='shippingPayer']")
    payer = Select(payer_selector)
    payer.select_by_index(shipping_info.payer)
    time.sleep(1)
    # method: int
    method_selector = driver.find_element_by_xpath("//select[@name='shippingMethod']")
    method = Select(method_selector)
    method.select_by_index(shipping_info.method)
    # from_area: int
    area_selector = driver.find_element_by_xpath("//select[@name='shippingFromArea']")
    area = Select(area_selector)
    area.select_by_index(shipping_info.from_area)
    # shipment_period: int
    duration_selector = driver.find_element_by_xpath("//select[@name='shippingDuration']")
    duration = Select(duration_selector)
    duration.select_by_index(shipping_info.duration)

def set_price(price: int):
    global driver
    driver.find_element_by_xpath("//input[@type='number']").send_keys(price)

def send_input():
    global driver
    driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(3)

def continue_sell():
    global driver
    driver.find_element_by_xpath("//button[contains(text(), '続けて出品する')]").click()

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def sell_item(item_info: Item_Info, shipping_info: Shipping_Info):
    set_item(item_info)
    set_delivery(shipping_info)
    set_price(item_info.price)


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def get_selling_list():
    global driver
    list_ul = driver.find_element_by_xpath("//ul[contains(@id, 'mypage-tab-transaction-now') and contains(@class, 'mypage-item-list')]")
    selling_list = list_ul.find_elements_by_tag_name("li")
    selling_items_url_list = []
    for item in selling_list:
        url = item.find_element_by_tag_name("a").get_attribute("href")
        print(url)
        selling_items_url_list.append(url)
    return selling_items_url_list

def delete_item(url):
    move_to_url(url)
    global driver
    delete_button = driver.find_element_by_xpath("//button[@data-modal='delete-item']")
    delete_button.click()
    print("a")
    # '削除する'要素が2個ある
    confirm_button = driver.find_elements_by_xpath("//button[contains(@type, 'submit') and contains(text(), '削除する')]")
    time.sleep(1)
    confirm_button[1].click()

def refresh_item_list(elapsed_date):
    # 日付処理
    border_date = dt.datetime.now() - dt.timedelta(days=elapsed_date)

    # 古い日付のアイテムのリストを取得(google spreadsheet？)
    # old_list = 

    # メルカリ上の出品リストを取得
    current_sell_list = get_selling_list()

    # 照合
    matched_list = []

    # 一致する場合は削除へ
    for item in matched_list:
        delete_item(item)

    # 一度Topに戻る
    move_to_top()

    # 再度アップロード


# main処理
def main():
    print("main")


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()