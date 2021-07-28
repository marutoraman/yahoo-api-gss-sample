from view import *

def test_saisyuppin():
    execute_sai_syuppin("1")
    
def test_price_down():
    execute_price_down(0.9)
    
def test_inport_syuppin_item():
    inport_syuppin_item_to_sheet()
    
    
def test_update_syuppin_stat():
    update_syuppin_stat()