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

class SpreadsheetManager():

    def __init__(self):
        self.worksheet = None


    def connect(self, file, sheet_no):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSONKEY, gspread.auth.DEFAULT_SCOPES)
        gs = gspread.authorize(credentials)
        worksheet = gs.open(file).get_worksheet(sheet_no)
        return worksheet


    def connect_by_sheetname(self, file_id, sheet_name):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSONKEY, gspread.auth.DEFAULT_SCOPES)
        gs = gspread.authorize(credentials)
        self.worksheet = gs.open_by_key(file_id).worksheet(sheet_name)


    def write(self, area, data):
        # data:2次元配列
        cell_list = self.worksheet.range(area)
        items = itertools.chain.from_iterable(data)
        for i, value in enumerate(items):
            cell_list[i].value = value
        self.worksheet.update_cells(cell_list)


    def write_to_column_from_df(self, column_name:str, df_data:pd.DataFrame,row:int,value:str):
        try:
            col = df_data.columns.get_loc(column_name)
            self.worksheet.update_cell(row + 1,col + 1,value)
        except Exception as e:
            logger.error(f"スプレッドシート書き込みエラー:{e}")


    def calculate_area(self, row, data):
        # data:2次元配列
        start_row = row + 1
        end_row = start_row + len(data) - 1
        start_cell = gspread.utils.rowcol_to_a1(start_row, 1)
        end_cell = gspread.utils.rowcol_to_a1(end_row, 9)
        area = start_cell + ":" + end_cell
        return area


    def fetch_all_data(self):
        try:
            data = self.worksheet.get_all_values() # セルに数式が埋め込まれている場合は数式を計算した結果を取得
            return data
        except Exception as e:
            if e.args[0].get('code') == 429:
                raise Exception("スプレッドシート更新回数の上限です")

    def fetch_all_data_to_df(self):
        try:
            data = self.fetch_all_data()
            if not data:
                raise Exception("data is None")
            return pd.DataFrame(data[1:], columns=data[0:1])
        except Exception as e:
            if e.args[0].get('code') == 429:
                raise Exception("スプレッドシート更新回数の上限です")


            
    def bulk_insert(self, datas:list):
        '''
        listを指定してスプレッドシートを一括更新
        '''
        begin_row = self.get_last_row() + 1 # 最終行の次の行から始める
        header = self.init_fetch_sheet_header()
        cells = self.worksheet.range(begin_row, 1, len(datas) + begin_row -1 , len(header))
        for row,data in enumerate(datas):
            for k,v in data.items():
                try:
                    col = header.index(k)
                    num = row*(len(header)) + col # 複数行にまたがるデータの場合でも１次元配列に格納されているため２次元→１次元に変換する
                    cells[num].value = v
                except Exception as e:
                    print(e)
                    pass

        self.worksheet.update_cells(cells)
        return True


    def _bulk_insert(self, datas:list, value_input_option='USER_ENTERED'):
        '''
        listを指定してスプレッドシートを一括更新
        '''
        begin_row = self.get_last_row() + 1 # 最終行の次の行から始める
        # list-dictから、dict-listに変換
        try:
            data_dict = {}
            for data in datas:
                for key,value in data.items():
                    if key not in data_dict:
                        data_dict[key] = []
                    data_dict[key].append(value)

            headers = self.init_fetch_sheet_header()
            
            # データをカラム毎のlist化して、カラム単位でupdateする
            # 全てのカラムを一括でupdateしてしまうと、想定外のセルがクリアされてしまう場合があるため
            for key,value_list in data_dict.items():
                col_num = headers.index(key)
                cells = self.worksheet.range(begin_row, col_num + 1, len(data_dict[key]) + begin_row -1 , col_num + 1)
                for row,data in enumerate(value_list):
                    try:
                        cells[row].value = data
                    except Exception as e:
                        print(e)
                        pass
                self.worksheet.update_cells(cells, value_input_option=value_input_option)
        except Exception as e:
            print(e.args[0].get('code') == 429)
            if e.args[0].get('code') == 429:
                raise Exception("スプレッドシート更新回数の上限です")
            else:
                raise Exception("スプレッドシート更新エラー")
                
        return True 


    def init_fetch_sheet_header(self, header_row: int=1):
        df = pd.DataFrame(self.worksheet.get_all_values())
        return list(df.loc[header_row-1,:]) 


    def get_last_row(self):
        '''
        最終行の取得
        '''
        return len(self.worksheet.get_all_values())
            
