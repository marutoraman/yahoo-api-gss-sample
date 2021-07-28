from io import open_code
import os
import time
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

if os.name == 'nt': #Windows
    DRIVER_NAME = "chromedriver.exe"
elif os.name == 'posix': #Mac
    DRIVER_NAME = "chromedriver"

def set_options():
    options = ChromeOptions()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile"))
    return options

def start_driver():
    options = set_options()
    return Chrome(ChromeDriverManager().install(), options=options)

def open_page(driver, url):
    print(f" ... going to open page [{url}]")
    driver.get(url)
    return driver

def close_driver(driver,):
    driver.close()

def quit_driver(driver):
    driver.quit()

def get_url(driver):
    url = driver.current_url
    return url

def wait_for_url(driver,url):
    while True:
        if driver.current_url == url:
            break
        print(f"次のURLが表示されるまで待機します:{url}")
        time.sleep(1)

# main処理
def main():
    print(" ... starting main")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
