from common.spread_sheet_manager import *


def test_connect():
    ss = SpreadsheetManager()
    ss.connect_by_sheetname(file_id="1ffjkOuMAqnd3Zz_cr0V_DqQiagzCC-DJSJzuv1Ldgw4", sheet_name="data")


def test_fetch_all_data():
    ss = SpreadsheetManager()
    ss.connect_by_sheetname(file_id="1ffjkOuMAqnd3Zz_cr0V_DqQiagzCC-DJSJzuv1Ldgw4", sheet_name="data")
    data = ss.fetch_all_data_to_df()
    print(data)


def test_bulk_insert():
    data = [
        {
            "name": "tset1",
            "price": 100,
            "review_average": 4.5,
            "review_count": 10,
            "thumbnail_url": "https://test.com"
        },
        {
            "name": "tset2",
            "price": 200,
            "review_average": 3.5,
            "review_count": 20,
            "thumbnail_url": "https://test2.com"
        }
    ]
    ss = SpreadsheetManager()
    ss.connect_by_sheetname(file_id="1mkHMaovwsNiZrLDteRao0Ec-NV_AwMRn6lJv9RIFNsg", sheet_name="item_list")
    ss.bulk_insert(data)