import eel, desktop
import spreadsheetManager, dataManager, fileManager
import mercari

app_name="html"
end_point="index.html"
size=(800,600)

@ eel.expose
def load_spreadsheet_list():
    file = 'spreadsheet_list.csv'
    spreadsheets = fileManager.read_csv_file(file)
    option_list = []
    for spreadsheet in spreadsheets:
        eel.add_option(spreadsheet[0])

@ eel.expose
def start(url: str):
    print("start button pressed")
    # 変数設定
    JSONKEY = 'testspreadsheet-302003-fb8fe37d15e6.json'

    # google spreadsheetに接続・データ抽出
    sheet = spreadsheetManager.connect_to(JSONKEY, url, 0)
    data = spreadsheetManager.fetch_allData(sheet)

    # まずはログイン
    mercari.login()
    
    # 抽出データの処理
    for datum in data:
        mercari.go_to_sell_page()

        item_info = dataManager.get_item_info(datum)
        delivery_info = dataManager.get_delivery_info(datum)

        ## 処理的なもの 出品 / 値下げ / 取下げ の条件分岐をここで datumにitemの状態(mercari_status)を表す値必要

        ## timer的なものがあるなら、ここに記述し、タイミングを図る

        mercari.sell_item(item_info, delivery_info)

    # ブラウザを閉じて終了
    mercari.close()


desktop.start(app_name,end_point,size)
