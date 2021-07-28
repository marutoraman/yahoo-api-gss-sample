import csv
import gspread, itertools
from datetime import datetime as dt
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from common.logger import set_logger
logger= set_logger(__name__)

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#JSONKEY = 'testspreadsheet-302003-fb8fe37d15e6.json'
JSONKEY = 'secrets/cred_spreadsheet.json'

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def connect_to(file, sheet_no):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSONKEY, gspread.auth.DEFAULT_SCOPES)
    gs = gspread.authorize(credentials)
    worksheet = gs.open(file).get_worksheet(sheet_no)
    return worksheet

def connect_to_sheetname(file_id, sheet_name):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSONKEY, gspread.auth.DEFAULT_SCOPES)
    gs = gspread.authorize(credentials)
    worksheet = gs.open_by_key(file_id).worksheet(sheet_name)
    return worksheet

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def get_last_row(sheet, column):
    column_data = sheet.col_values(column)
    last_row_index = len(column_data)
    return last_row_index

def write(sheet, area, data):
    # data:2次元配列
    cell_list = sheet.range(area)
    items = itertools.chain.from_iterable(data)
    for i, value in enumerate(items):
        cell_list[i].value = value
    sheet.update_cells(cell_list)

def write_to_column_from_df(sheet:Worksheet,column_name:str, df_data:pd.DataFrame,row:int,value:str):
    try:
        col = df_data.columns.get_loc(column_name)
        sheet.update_cell(row + 1,col + 1,value)
    except Exception as e:
        logger.error(f"スプレッドシート書き込みエラー:{e}")
        
## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def now_time():
    now_datetime = dt.now()
    string_datetime = now_datetime.strftime('%Y/%m/%d')
    return string_datetime

def calculate_area(row, data):
    # data:2次元配列
    start_row = row + 1
    end_row = start_row + len(data) - 1
    start_cell = gspread.utils.rowcol_to_a1(start_row, 1)
    end_cell = gspread.utils.rowcol_to_a1(end_row, 9)
    area = start_cell + ":" + end_cell
    return area

## _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

def fetch_allData(worksheet):
    try:
        data = worksheet.get_all_values() # セルに数式が埋め込まれている場合は数式を計算した結果を取得
        return data
    except Exception as e:
        if e.args[0].get('code') == 429:
            raise Exception("スプレッドシート更新回数の上限です")

        
def bulk_update_row(worksheet, datas:list, begin_row:int):
    '''
    listを指定してスプレッドシートを一括更新
    '''
    header = init_fetch_sheet_header(worksheet)
    cells = worksheet.range(begin_row, 1, len(datas) + begin_row -1 , len(header))
    for row,data in enumerate(datas):
        for k,v in data.items():
            try:
                col = header.index(k)
                num = row*(len(header)) + col # 複数行にまたがるデータの場合でも１次元配列に格納されているため２次元→１次元に変換する
                cells[num].value = v
            except Exception as e:
                print(e)
                pass

    worksheet.update_cells(cells)
    return True


def bulk_update_row2(worksheet, datas:list, begin_row:int, value_input_option='USER_ENTERED'):
    '''
    listを指定してスプレッドシートを一括更新
    '''
    # list-dictから、dict-listに変換
    try:
        data_dict = {}
        for data in datas:
            for key,value in data.items():
                if key not in data_dict:
                    data_dict[key] = []
                data_dict[key].append(value)

        headers = init_fetch_sheet_header(worksheet)
        
        # データをカラム毎のlist化して、カラム単位でupdateする
        # 全てのカラムを一括でupdateしてしまうと、想定外のセルがクリアされてしまう場合があるため
        for key,value_list in data_dict.items():
            col_num = headers.index(key)
            cells = worksheet.range(begin_row, col_num + 1, len(data_dict[key]) + begin_row -1 , col_num + 1)
            for row,data in enumerate(value_list):
                try:
                    cells[row].value = data
                except Exception as e:
                    print(e)
                    pass
            worksheet.update_cells(cells, value_input_option=value_input_option)
    except Exception as e:
        print(e.args[0].get('code') == 429)
        if e.args[0].get('code') == 429:
            raise Exception("スプレッドシート更新回数の上限です")
        else:
            raise Exception("スプレッドシート更新エラー")
            
    return True 


def init_fetch_sheet_header(worksheet):
    '''
    ２行目をシステム用がカラムを判別するのに使用する運用のため
    '''
    df = pd.DataFrame(worksheet.get_all_values())
    return list(df.loc[0,:]) # 1行目をシステム用のヘッダとする


def get_last_row(worksheet):
    '''
    最終行の取得
    '''
    return len(worksheet.get_all_values())
           

if __name__ == "__main__":
    main()