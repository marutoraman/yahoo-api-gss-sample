import eel, desktop
import os, spreadsheetManager

app_name="html"
end_point="index.html"
size=(800,600)

@ eel.expose
def start(url):

    print("start")

    # 変数設定
    JSONKEY = 'testspreadsheet-302003-fb8fe37d15e6.json'
    FILE = 'testspreadsheet'

    sheet = spreadsheetManager.connect_to(JSONKEY, url, 0)
    data = spreadsheetManager.fetch_allData(sheet)
    print(data)



desktop.start(app_name,end_point,size)
