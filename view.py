import eel, desktop
import os, spreadsheetManager, fileManager

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
def start(url, start_time, interval_time):
    print("start button pressed")
    print(start_time) # YYYY-mm-ddTHH:MM
    print(interval_time) # XX:XX
    # 変数設定
    JSONKEY = 'testspreadsheet-302003-fb8fe37d15e6.json'

    sheet = spreadsheetManager.connect_to(JSONKEY, url, 0)
    data = spreadsheetManager.fetch_allData(sheet)    
    print(data)



desktop.start(app_name,end_point,size)
