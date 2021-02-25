import csv
import gspread, itertools
from datetime import datetime as dt
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def connect_to(jsonKey, file, sheet):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonKey, scope)
    gs = gspread.authorize(credentials)
    worksheet = gs.open(file).get_worksheet(sheet)
    return worksheet

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def get_last_row(sheet, column):
    column_data = sheet.col_values(column)
    last_row_index = len(column_data)
    return last_row_index

def write(sheet, area, data):
    cell_list = sheet.range(area)
    items = itertools.chain.from_iterable(data)
    for i, value in enumerate(items):
        cell_list[i].value = value
    sheet.update_cells(cell_list)

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def now_time():
    now_datetime = dt.now()
    string_datetime = now_datetime.strftime('%Y/%m/%d')
    return string_datetime

def calculate_area(row, data):
    start_row = row + 1
    end_row = start_row + len(data) - 1
    start_cell = gspread.utils.rowcol_to_a1(start_row, 1)
    end_cell = gspread.utils.rowcol_to_a1(end_row, 9)
    area = start_cell + ":" + end_cell
    return area

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def fetch_unsearced_url():
    ## 接続情報
    jsonKey = 'testspreadsheet-302003-fb8fe37d15e6.json'
    file = 'testspreadsheet'
    workSheet1 = connect_to(jsonKey, file, 1)
    keyword_data = workSheet1.get_all_values()
    unsearched_urls = []
    for datum in keyword_data:
        if datum[7] == "未":
            unsearched_urls.append(datum[3]) 
    return unsearched_urls

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def write_url_data(data):
    ## 先頭行(見出し)の削除
    del data[0]

    ## 接続情報
    jsonKey = 'testspreadsheet-302003-fb8fe37d15e6.json'
    file = 'testspreadsheet'

    # 必要データ取得
    workSheet1 = connect_to(jsonKey, file, 1)
    keyword_data = workSheet1.get_all_values()
    workSheet0 = connect_to(jsonKey, file, 0)
    url_data = workSheet0.get_all_values()
    last_row = len(url_data)

    # 重複チェック
    for datum in url_data:
        if datum[3] == data[0][0]:
            print(" すでにそのurlは検索済みです ")
            return

    # データ形成
    data_index = last_row
    url = data[0][0]
    authority = ""
    for datum in keyword_data:
        if url == datum[3]:
            authority = datum[5]
    now = now_time()

    ## データの変更
    ## [url, title, キーワード, Vol, ポジション, 流入見込み, SD]から
    ## [no, domain(url), Authority, キーワード, Vol, position, 流入見込, SD]へ
    formatted_data = []
    for datum in data:
        formatted_data.append([str(data_index), datum[0], authority, datum[2], datum[3], datum[4], datum[5], datum[6], now])
        data_index += 1

    ## 書き込むcellの計算
    area = calculate_area(last_row, formatted_data)
    
    # 書き込み
    write(workSheet0, area, formatted_data)

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def write_keyword_data(data):

    # 接続、必要データ取得
    jsonKey = 'testspreadsheet-302003-fb8fe37d15e6.json'
    file = 'testspreadsheet'
    workSheet1 = connect_to(jsonKey, file, 1)
    keyword_data = workSheet1.get_all_values()
    last_row = len(keyword_data)

    # 重複チェック
    for datum in keyword_data:
        if datum[2] == data[0][0]:
            print(" same keyword exists")
            return

    # データの形成
    data_index = last_row
    url_research = "未"
    ## data = [keyword, counter, domain, title, authority] を
    ## [number, keyword, counter, domain title, authority, url_research]
    now = now_time()
    formatted_data = []
    for datum in data:
        formatted_data.append([str(data_index), datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], now, url_research])
        data_index += 1

    ## 書き込むcellの計算
    area = calculate_area(last_row, formatted_data)
    
    # 書き込み
    write(workSheet1, area, formatted_data)

# main処理
def main():
    print("main")
    a = get_last_row()
    print(a)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()