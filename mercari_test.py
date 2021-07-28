from mercari import *
import datetime

def test_check_saisyuppin():
    dt = datetime.datetime.strptime("2021/04/07 00:00:00","%Y/%m/%d %H:%M:%S")
    print(check_sai_syuppin_date(dt,1))
    

def test_price_down():
    start()
    price_down("m51667636888")
    

def test_fetch_syuppin_item():
    start()
    try:
        login()
    except:
        pass
    fetch_syuppin_item_data()
    

def test_fetch_syuppin_stat():
    ids = ["m20059788993","m67844195750","m29670018868"]
    res = fetch_syuppin_stat(ids)
    print(res)