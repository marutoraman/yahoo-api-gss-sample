from dataManager import Item_Info, Delivery_Info
import driverManager

URL = "https://www.mercari.com/jp/"
SELL_URL = "https://www.mercari.com/jp/sell"

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def login():
    global driver
    driver = driverManager.start_driver()
    driver = driverManager.open_page(driver, URL)
    driver.find_element_by_link_text("ログイン").click()

def close():
    global driver
    driverManager.close_driver(driver)
    driverManager.quit_driver(driver)

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def go_to_sell_page():
    global driver
    driver = driverManager.open_page(driver, SELL_URL)

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def set_item(item_info: Item_Info):
    global driver
    # image folder ???
    # driver.find_element_by_xpath ????? ## ここ修正必要
    # title: str
    driver.find_element_by_xpath("//input[contains(@type='text') and contains(@name='name')]").send_keys(item_info.title)
    # detail: str
    driver.find_element_by_xpath("//textarea[@name='description']").send_keys(item_info.detail)
    # category: int
    category_selector = driver.find_element_by_xpath("//select[@name='categoryId']")
    category_selector.select_by_index(item_info.category)
    # brand: str
    driver.find_element_by_xpath("//input[contains(@type='text') and contains(@name='brandName')]").send_keys(item_info.brand)
    # status: int
    status_selector = driver.find_element_by_xpath("//select[@name='itemCondition']")
    status_selector.select_by_index(item_info.status)    

def set_delivery(delivery_info: Delivery_Info):
    global driver
    # payer: int
    payer_selector = driver.find_element_by_xpath("//select[@name='shippingPayer']")
    payer_selector.select_by_index(delivery_info.payer)
    # send_from: int
    area_selector = driver.find_element_by_xpath("//select[@name='shippingFromArea']")
    area_selector.select_by_index(delivery_info.send_from)
    # shipment_period: int
    shipment_selector = driver.find_element_by_xpath("//select[@name='shippingDuration']")
    shipment_selector.select_by_index(delivery_info.shipment_period)

def set_price(price: int):
    global driver
    driver.find_element_by_xpath("//input[@type='number']").send_keys(price)

def send_input():
    global driver
    driver.find_element_by_xpath("//button[@type='submit']").click()

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def sell_item(item_info: Item_Info, delivery_info: Delivery_Info):
    set_item(item_info)
    set_delivery(delivery_info)
    set_price(item_info.price)
    send_input()

# main処理
def main():
    print("main")


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()