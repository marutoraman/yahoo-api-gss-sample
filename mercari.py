from fetch_mercari_item import FetchMercariItem
import os, glob, time
import datetime as dt

from pandas.core.frame import DataFrame
from dataManager import Item_Info, Shipping_Info
import driverManager
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as bs
import base64

from gdrive import *

from common.logger import set_logger
logger= set_logger(__name__)


TOP = "https://www.mercari.com/jp/"
SELL_URL = "https://www.mercari.com/jp/sell/"
SELLING_URL = "https://www.mercari.com/jp/mypage/listings/listing/"
MYPAGE_ITEM_URL = "https://www.mercari.com/jp/mypage/items/"
SELL_EDIT_URL = "https://www.mercari.com/jp/sell/edit/"
ITEM_URL = "https://www.mercari.com/jp/items/"

SELL_ITEM = "出品中"
NO_SELL_ITEM = "販売終了"

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def start():
    global driver
    driver = driverManager.start_driver()
    driver = driverManager.open_page(driver, TOP)
    return driver

def login():
    global driver
    driver.find_element_by_link_text("ログイン").click()
    driverManager.wait_for_url(driver,TOP)

def close():
    global driver
    driverManager.close_driver(driver)
    driverManager.quit_driver(driver)


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def check_status():
    global driver
    move_to_url(SELL_URL)
    while True:
        if driver.current_url == SELL_URL:
            print("SELL_URLに移動できたのでループ終了")
            break
        else:
            print("SELL_URLではないので、5秒待機し、再度urlを確認")
            time.sleep(5)

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

def set_item(item_info: Item_Info, drive_id:str, image_upload_wait_time:int=1):
    global driver
    g = Gdrive(drive_id)
    # GoogleDriveから画像を取得
    g.download_file("img", f"item-{item_info.image_file_name}") # GoogleDriveから画像をダウンロード
    image_files = glob.glob(os.path.join(os.getcwd(),"img",f"item-{item_info.image_file_name}.*"))
    # 画像アップロード
    for image in image_files[:10]: # 画像は最大１０枚まで
        # multiple属性が付与されていると画像が重複してUPされるため削除する
        driver.execute_script("""document.querySelector("[type='file']").removeAttribute('multiple')""")
        elm = driver.find_element_by_css_selector("[type='file']")
        elm.send_keys(image)
        time.sleep(image_upload_wait_time)

    
    # title: str    
    driver.find_element_by_xpath("//input[contains(@type, 'text') and contains(@name, 'name')]").send_keys(item_info.title)
    
    # detail: str
    driver.find_element_by_xpath("//textarea[@name='description']").send_keys(item_info.detail)
    
    # main_category: int
    category_selector = driver.find_elements_by_xpath("//select[@name='categoryId']")
    main_category = Select(category_selector[0])
    main_category.select_by_visible_text(item_info.main_category)
    # sub_category: int
    time.sleep(1)
    category_selector = driver.find_elements_by_xpath("//select[@name='categoryId']")
    sub_category = Select(category_selector[1])
    sub_category.select_by_visible_text(item_info.sub_category)
    
    # category_detail: int
    time.sleep(1)
    try:
        category_selector = driver.find_elements_by_xpath("//select[@name='categoryId']")
        category_detail = Select(category_selector[2])
        category_detail.select_by_visible_text(item_info.category_detail)
    except:
        pass
    
    # size: strで指定
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//select[@name='size']").send_keys(item_info.size)
        #size = Select(size_selector)
        #size.select_by_index(item_info.size)
    except:
        pass
    
    # brand: str 非必須
    driver.find_element_by_xpath("//input[contains(@type, 'text') and contains(@name, 'brandName')]").send_keys(item_info.brand)
    time.sleep(3)
    
    # 複数HITする場合は選択肢が表示されるので、一番上をクリックする
    _selection_elms = driver.find_elements_by_xpath("//li[contains(@id, 'brand-')]")
    if len(_selection_elms) >= 1:
        _selection_elms[0].click()
    time.sleep(30)
    
    # status: int
    status_selector = driver.find_element_by_xpath("//select[@name='itemCondition']")
    status = Select(status_selector)
    status.select_by_visible_text(item_info.status)
    
    # 画像削除
    for image in image_files:
        os.remove(image) 

def set_delivery(shipping_info: Shipping_Info):
    global driver
    # payer: int
    payer_selector = driver.find_element_by_xpath("//select[@name='shippingPayer']")
    payer = Select(payer_selector)
    payer.select_by_visible_text(shipping_info.payer)
    time.sleep(1)
    # method: int
    method_selector = driver.find_element_by_xpath("//select[@name='shippingMethod']")
    method = Select(method_selector)
    method.select_by_visible_text(shipping_info.method)
    # from_area: int
    area_selector = driver.find_element_by_xpath("//select[@name='shippingFromArea']")
    area = Select(area_selector)
    area.select_by_visible_text(shipping_info.from_area)
    # shipment_period: int
    duration_selector = driver.find_element_by_xpath("//select[@name='shippingDuration']")
    duration = Select(duration_selector)
    duration.select_by_visible_text(shipping_info.duration)

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


def fetch_item_id():
    global driver
    item_link = None
    for i in range(5):
        try:
            elms = driver.find_elements_by_partial_link_text("出品した商品をみる")
            if len(elms) >= 1:
                item_link = elms[0].get_attribute("href")
                break
        except:
            time.sleep(0.2)
            
    return item_link.split("/")[-2] if item_link else ""


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def sell_item(item_info: Item_Info, shipping_info: Shipping_Info,drive_id:str,image_upload_wait_time:int=1):
    set_item(item_info,drive_id,image_upload_wait_time)
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
    # '削除する'要素が2個ある
    confirm_button = driver.find_elements_by_xpath("//button[contains(@type, 'submit') and contains(text(), '削除する')]")
    time.sleep(1)
    confirm_button[1].click()

def delete_syuppin_item(item_id:str):
    global driver
    # 出品削除
    logger.info(f"出品ID:{item_id}")
    driver.get(f"{MYPAGE_ITEM_URL}/{item_id}")
    driver.find_element_by_css_selector("[data-modal='delete-item']").click()
    driver.find_elements_by_xpath("//button[contains(@type, 'submit') and contains(text(), '削除する')]")[1].click()


def price_down(item_id:str,new_price:int):
    global driver
    logger.info(f"出品ID:{item_id} / new_price:{new_price}")
    driver.get(f"{SELL_EDIT_URL}/{item_id}")
    time.sleep(5)
    driver.find_elements_by_css_selector("input")[-1].clear()
    time.sleep(5)
    driver.find_elements_by_css_selector("input")[-1].send_keys(new_price)
    time.sleep(2)
    driver.find_element_by_css_selector("button[type='submit']").click()


def check_sai_syuppin_date(syuppin_date,sai_syuppin_date):
    return (dt.datetime.now() - syuppin_date).total_seconds() > sai_syuppin_date * 86400

def check_syuppin_stat(item_id:str):
    global driver
    driver.get(MYPAGE_ITEM_URL + item_id)
    if len(driver.find_elements_by_css_selector(".error-image")):
        return NO_SELL_ITEM
    

def fetch_syuppin_item(item_limit:int=1000, page_limit:int=100):
    global driver
    start()
    try:
        login()
    except:
        pass
    driver.get(SELLING_URL)
    urls = []
    page_count = 0
    while True:
        if page_count > page_limit:
            break     
        try:   
            if driver.find_element_by_css_selector(".mypage-item-not-found").text.find("出品中の商品がありません") >= 0:
                logger.info("これ以上、商品がないため終了")
                break
        except:
            pass
        # 出品URL取得
        item_elms = driver.find_elements_by_css_selector('#mypage-tab-transaction-now li')
        try:
            # 公開中の出品が対象
            for elm in item_elms:
                try:
                    item_link = elm.find_element_by_css_selector('a').get_attribute('href')
                    if elm.find_element_by_css_selector(".mypage-item-status").text.find("公開停止中")< 0:
                        logger.info(f"出品中商品:{item_link}")
                        urls.append(item_link)
                    else:
                        logger.info(f"公開停止商品のためスキップ:{item_link}")
                except Exception as e:
                    logger.error(f"出品商品取得エラー:{e}")
            
        except:
            logger.info("出品情報取得エラー > ページ終了と判断して終了")
            break
        # 次ページに遷移
        next_page_elms = driver.find_elements_by_css_selector('.pager-next.pager-cell a')
        try:
            logger.info(f"次のページへ:{next_page_elms[0].get_attribute('href')}")
            driver.get(next_page_elms[0].get_attribute('href'))
            time.sleep(3)
        except Exception as e:
            logger.error(f"次ページ切り替えエラー:{e}")
            break
        page_count += 1
    
    close()
    
    # 商品情報取得
    items = FetchMercariItem.fetch_mercari_items(urls[:item_limit])
    return items


def fetch_syuppin_stat(ids:list):
    driver = driverManager.start_driver()
    
    syuppin_stats = []
    prices = []
    for id in ids:
        # 出品前の場合はスキップして空白を返す
        if len(id) <= 1:
            syuppin_stats.append("")
            prices.append("")
            continue
            
        driver.get(ITEM_URL + id)
        soup = bs(driver.page_source, "html.parser")
        sold_out_elms = driver.find_elements_by_css_selector(".item-main-content .item-sold-out-badge")
        buy_btn_elms = driver.find_elements_by_css_selector(".item-buy-btn")
        #item_price_elms = driver.find_elements_by_css_selector(".item-price")
        item_price_elm = soup.select_one(".item-price") # 値がうまく取れないためbsを使用
        deleted_item_elms = driver.find_elements_by_css_selector(".deleted-item-name")
        # 販売済
        if len(sold_out_elms) >= 1:
            logger.info(f"販売済:{id}")
            syuppin_stats.append("販売済")
        # 公開停止/削除
        elif len(deleted_item_elms) >= 1:
            logger.info(f"公開停止/削除:{id}")
            syuppin_stats.append(f"公開停止/削除")
        # 出品中
        else:
            logger.info(f"出品中:{id}")
            syuppin_stats.append("出品中")

        # 現在価格
        if item_price_elm != None: 
            prices.append(item_price_elm.text.replace("¥","").replace(",",""))
        else:
            prices.append("")

    driver.quit()
    
    return syuppin_stats,prices

    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    pass