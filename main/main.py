import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv
load_dotenv() #環境変数のロード

from common.spread_sheet_manager import SpreadsheetManager
from engine.yahoo import YahooAPI

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]

def main():
    # jan一覧の取得
    ss = SpreadsheetManager()
    ss.connect_by_sheetname(SPREADSHEET_ID, "jan_list")
    jan_df = ss.fetch_all_data_to_df()
    jan_list = jan_df["jan"].values.tolist()
    
    #YahooAPI
    items = []
    for jan in jan_list:
        print(jan)
        item = YahooAPI.fetch_item(jan[0])
        if item:
            items.append(item.__dict__)

    # 書き込み
    print(items)
    ss.connect_by_sheetname(SPREADSHEET_ID, "item_list")
    ss.bulk_insert(items)


main()