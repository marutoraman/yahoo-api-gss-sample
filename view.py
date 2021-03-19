import eel, desktop, time
from datetime import datetime as dt
import spreadsheetManager, dataManager, fileManager
import mercari

app_name="html"
end_point="index.html"
size=(800,600)

@ eel.expose
def load_spreadsheet_list():
    file = 'spreadsheet_list.csv'
    spreadsheets = fileManager.read_csv(file)
    option_list = []
    for spreadsheet in spreadsheets:
        eel.add_option(spreadsheet[0])

@ eel.expose
def start(spreadsheet_number: int, start_time: str, interval_time: str):
    print("start button pressed")

    # 変数設定
    spreadsheet_list = fileManager.read_csv("spreadsheet_list.csv")
    URL = spreadsheet_list[spreadsheet_number][0]
    JSONKEY = spreadsheet_list[spreadsheet_number][1]

    # google spreadsheetに接続・データ抽出
    sheet = spreadsheetManager.connect_to(JSONKEY, URL, 0)
    sheet_data = spreadsheetManager.fetch_allData(sheet)

    # headerとdataを分離する
    header = sheet_data[0]
    data = sheet_data[1:]

    # ログインは不要
    mercari.start()

    # 初回ログイン用にURL判別
    mercari.check_status()
    
    # 開始時間設定
    if len(start_time) != 0: # YYYY-mm-ddTHH:MM
        trigger_time = dt.strptime(start_time, "%Y-%m-%dT%H:%M")
        while True:
            left_time = trigger_time - dt.now()
            print(f"出品開始まで ... {left_time}")
            if float(left_time.total_seconds()) < 0.0:
                print("時間になったので、出品処理を開始します。")
                break
            else:
                time.sleep(1)

    # 抽出データの処理
    for row, datum in enumerate(data):
        print('datum:', datum)
        mercari.go_to_sell_page()

        item_info = dataManager.get_dummy_item_info() # get_item_info(datum)
        delivery_info = dataManager.get_dummy_shippment_info() # get_delivery_info(datum)

        ## 出品時間を決めたいならここにタイマー

        ## 処理的なもの 出品 / 値下げ / 取下げ の条件分岐をここで datumにitemの状態(mercari_status)を表す値必要
        mercari.sell_item(item_info, delivery_info)
        mercari.send_input()

        if row != len(data) - 1:
            # 出品時間間隔の設定
            if len(interval_time) > 0:
                wait_time_component = interval_time.split(":")
                minutes = int(wait_time_component[0])
                seconds = int(wait_time_component[1])
                total_wait_seconds = minutes * 60 + seconds 
                print(f"次の出品まで {total_wait_seconds} 秒待つよ")
                time.sleep(total_wait_seconds)
            print("出品時間になったので、次の出品へ")
            
            mercari.continue_sell()

        # DEBUG設定
        if row == 1:
            break

    # ブラウザを閉じて終了
    mercari.close()

@ eel.expose
def reSell(elapsed_date: str):
    if not elapsed_date.isdecimal():
        print(f"入力値: {elapsed_date} は数値ではありません")
        return
    elif int(elapsed_date) == 0:
        print(f"入力値が [0] なので、何もしません")
        return

    mercari.start()
    mercari.refresh_item_list()


desktop.start(app_name,end_point,size)
