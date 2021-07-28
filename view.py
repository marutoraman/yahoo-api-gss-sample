import os
import eel, desktop, time
from datetime import datetime as dt
import pandas as pd
import spreadsheetManager, dataManager, fileManager
import mercari
from common.my_util import now_string
import random
import schedule

from dotenv import load_dotenv
load_dotenv()

from common.logger import set_logger
logger= set_logger(__name__)


app_name="html"
end_point="index.html"
size=(800,600)

def load_spreadsheet():
    file = 'sheet_setting.csv'
    spreadsheets = fileManager.read_csv(file)

    if len(spreadsheets) >=1:
        # urlからスプレッドシートidを取得
        return spreadsheets[1][0].split("/")[-2]
    else:
        raise Exception("スプレッドシート設定が読み取れません")
    
def load_drive_id():
    file = 'sheet_setting.csv'
    drive_url = fileManager.read_csv(file)

    if len(drive_url) >=1:
        # urlからdrive_idを取得
        _id = drive_url[1][1].split("/")[-1]
        return _id[:_id.find("?")]
    else:
        raise Exception("DriveID設定が読み取れません")

@ eel.expose
def start(interval_min_time: int,interval_max_time: int, image_upload_wait_time:int=1):
    print("start button pressed")

    # google spreadsheetに接続・データ抽出
    #sheet = spreadsheetManager.connect_to(JSONKEY, URL, 0)
    sheet_id = load_spreadsheet()
    drive_id = load_drive_id()
    print(sheet_id, drive_id)
    sheet = spreadsheetManager.connect_to_sheetname(sheet_id, "data")
    sheet_data = spreadsheetManager.fetch_allData(sheet)
    # headerとdataを分離する
    header = sheet_data[0]
    data = sheet_data[1:]
    df = pd.DataFrame(data,columns=header)

    # 共通情報
    sheet2 = spreadsheetManager.connect_to_sheetname(sheet_id, "common_setting")
    sheet_data2 = spreadsheetManager.fetch_allData(sheet2)
    df_common = pd.DataFrame(sheet_data2[1:], columns=sheet_data2[0])
    common_setting = df_common[0:]

    # ログインは不要
    mercari.start()

    # 初回ログイン用にURL判別
    mercari.check_status()

    # 抽出データの処理
    count = 0
    fail_count = 0
    logger.info(f"出品件数:{len(df)}")
    for row, datum in df.iterrows():
        logger.info(f"出品開始:{row}")
        try:
            # 出品中の場合はスキップ
            if datum["出品"].find("出品中") >= 0:
                logger.info(f"既に出品中のためスキップ:{row}")
                continue
            if datum["出品有無"] != "◯":
                logger.info(f"出品対象外のためスキップ:{row}")
                continue
            # 出品終了チェック
            if datum["出品"] in ["公開停止","販売済"]:
                logger.error(f"出品が終了しています / row:{row}")
                continue
            mercari.go_to_sell_page()

            # 本番用データ
            item_info = dataManager.get_item_info(sheet_id, 0, header, datum)
            delivery_info = dataManager.get_delivery_info(common_setting)

            ## 各出品時間を決めたいならここにタイマー

            ## 処理(出品する)
            mercari.sell_item(item_info, delivery_info, drive_id, image_upload_wait_time)
            mercari.send_input()
            item_id = mercari.fetch_item_id()
            
            if row != len(data) - 1:
                mercari.continue_sell()
                
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df, row=int(row)+1, value="出品中")
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品日時", df_data=df, row=int(row)+1, value=now_string())
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品ID", df_data=df, row=int(row)+1, value=item_id)
            spreadsheetManager.write_to_column_from_df(sheet, column_name="現在価格", df_data=df, row=int(row)+1, value=datum["出品開始金額"])
            logger.info(f"出品完了:{row} / 出品ID:{item_id} / title:{item_info.title} / price:{item_info.price}")
            count += 1
            
            # 出品時間間隔の設定
            if interval_max_time != "" and interval_min_time != "":
                interval = random.randint(interval_min_time, interval_max_time)
                logger.info(f"待ち時間:{interval}分")
                time.sleep(interval*60)
        
        except Exception as e:
            import traceback
            logger.error(f"出品失敗:{row} / {traceback.format_exc()}")
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df, row=int(row)+1, value="出品エラー")
            fail_count += 1
            
    # ブラウザを閉じて終了
    mercari.close()

    # eelに通知
    eel.popup_alert(f"出品が完了しました: 完了件数:{count} 件 / 失敗件数:{fail_count} 件")

@ eel.expose
def execute_sai_syuppin(image_upload_wait_time:int=1):
    # 現在の出品ステータスを取得して更新
    #update_syuppin_stat()
    
    # 再出品用データ読み込み
    sheet_id = load_spreadsheet()
    drive_id = load_drive_id()
    sheet = spreadsheetManager.connect_to_sheetname(sheet_id, "data")
    sheet_data = spreadsheetManager.fetch_allData(sheet)
    df_data = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])
    df_data = df_data[0:]
    # 共通項目シートの読み込み
    sheet2 = spreadsheetManager.connect_to_sheetname(sheet_id, "common_setting")
    sheet_data2 = spreadsheetManager.fetch_allData(sheet2)
    df_common = pd.DataFrame(sheet_data2[1:], columns=sheet_data2[0])
    common_setting = df_common[0:]
    
    # 再出品
    mercari.start()
    mercari.check_status()
    count = 0
    for row,item in df_data.iterrows():
        try:
            # 出品IDチェック
            if item["出品ID"] == "":
                logger.error(f"出品IDが空です / row:{row}")
                continue
            if item["再出品有無"] != "◯":
                logger.info(f"再出品対象外のためスキップ:{row}")
                continue
            # 販売済チェック
            try:
                if item["出品"] in ["販売済"]:
                    logger.error(f"出品が終了しています / row:{row}")
                    continue
            except:
                pass
            
            # 出品削除
            try:
                mercari.delete_syuppin_item(item["出品ID"])
            except:
                logger.info(f"出品削除が失敗しました / row:{row} / id:{item['出品ID']}")
                
            try:
                # 再度出品          
                mercari.go_to_sell_page()
                item_info = dataManager.get_item_info(sheet_id, 0, sheet_data[0], item)
                delivery_info = dataManager.get_delivery_info(common_setting)
                # 出品処理
                mercari.sell_item(item_info, delivery_info, drive_id, image_upload_wait_time)
                mercari.send_input()
                item_id = mercari.fetch_item_id()
            except:
                logger.error(f"再出品エラー / row:{row}")
                spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df_data, row=int(row)+1, value='再出品エラー')
                continue
            
            if item_id == "":
                logger.error(f"出品IDが確認できませんでした / row:{row}")
                spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df_data, row=int(row)+1, value='再出品エラー')
                continue
            
            # スプレッドシート更新
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df_data, row=int(row)+1, value=f'=hyperlink("{mercari.MYPAGE_ITEM_URL}/{item_id}","出品中")')
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品日時", df_data=df_data, row=int(row)+1, value=now_string())
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品ID", df_data=df_data, row=int(row)+1, value=item_id)
            spreadsheetManager.write_to_column_from_df(sheet, column_name="現在価格", df_data=df_data, row=int(row)+1, value=item["出品開始金額"])
            logger.info(f"再出品完了 / row:{row} / 出品ID:{item_id} ")
            count += 1
        except:
            import traceback
            logger.error(f"出品失敗:{row} / {traceback.format_exc()}")
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df_data, row=int(row)+1, value="出品エラー")

    mercari.close()
    
    # eelに通知
    eel.popup_alert(f"再出品が完了しました: 再出品完了件数 {count} 件")

@ eel.expose
def execute_price_down(price_down_yen:int, price_down_min_interval:int, price_down_max_interval:int):
    # 現在の出品ステータスを取得して更新
    #update_syuppin_stat()
    
    # 再出品用データ読み込み
    sheet_id = load_spreadsheet()
    sheet = spreadsheetManager.connect_to_sheetname(sheet_id, "data")
    sheet_data = spreadsheetManager.fetch_allData(sheet)
    df_data = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])
    df_data = df_data[0:]
    
    # 値下げ
    mercari.start()
    mercari.check_status()
    count = 0
    for row,item in df_data.iterrows():
        try:
            # 値下げ禁止チェック
            if item["値下げ有無"] != "◯":
                logger.error(f"値下げ対象外商品です / row:{row}")
                continue
            # 出品IDチェック
            if item["出品ID"] == "":
                logger.error(f"出品IDが空です / row:{row}")
                continue
            # 出品終了チェック
            if item["出品"] in ["公開停止","販売済"]:
                logger.error(f"出品が終了しています / row:{row}")
                continue
            # 値下げ価格算出
            now_price = int(item['現在価格']) if item['現在価格'] != "" else int(item["出品開始金額"]) # 新価格設定
            new_price = now_price - price_down_yen
            if new_price < 300:
                logger.error(f"300円より安く設定はできません / row:{row} / new_price:{new_price}")
                continue
            # 損益分岐点チェック
            _limit = int(item["値下停止額"]) if item["値下停止額"] != "" else 0
            if new_price < _limit : # 損益分岐点を下回るなら値下げしない
                logger.error(f"利益が出ないため値下げはできません / row:{row} / new_price:{new_price} / 値下停止額:{_limit}")
                continue
            mercari.price_down(item['出品ID'], new_price)
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df_data, row=int(row)+1, value="出品中")
            spreadsheetManager.write_to_column_from_df(sheet, column_name="現在価格", df_data=df_data, row=int(row)+1, value=str(new_price))
            logger.info(f"値下げ完了 / row:{row} / 出品ID:{item['出品ID']}")
            
            # 指定した時間の間でランダムに待つ
            interval = random.randint(price_down_min_interval,price_down_max_interval)
            logger.info(f"待ち時間:{interval}分")
            time.sleep(interval*60)
            time.sleep(3) # 最低でも3秒待つ
            count += 1
        except:
            import traceback
            logger.error(f"値下げ失敗:{row} / {traceback.format_exc()}")
            spreadsheetManager.write_to_column_from_df(sheet, column_name="出品", df_data=df_data, row=int(row)+1, value="値下げエラー")
        

    mercari.close()
    
    # eelに通知
    eel.popup_alert(f"値下げが完了しました: 値下げ完了件数 {count} 件")
    
@eel.expose
def execute_price_down_schedule_loop(start_time,price_down_yen,price_down_min_interval, price_down_max_interval):
    if start_time == "":
        logger.info(f"値下げ処理 即時開始")
        execute_price_down(price_down_yen=price_down_yen,
                           price_down_min_interval=price_down_min_interval,
                           price_down_max_interval=price_down_max_interval)
        return True
    logger.info(f"値下げ処理開始時間:{start_time}")
    schedule.every().day.at(start_time).do(execute_price_down, 
                                        price_down_yen=price_down_yen,
                                        price_down_min_interval=price_down_min_interval,
                                        price_down_max_interval=price_down_max_interval)
    while True:
        logger.info("値下げ処理開始を待ち受けています・・・")
        schedule.run_pending()
        time.sleep(60)
        
    

@eel.expose
def import_syuppin_item_to_sheet():
    '''
    メルカリに既に出品中のアイテムを収集してスプレッドシートに書き込み
    '''
    sheet_id = load_spreadsheet()
    sheet = spreadsheetManager.connect_to_sheetname(sheet_id, "data")
    sheet_data = spreadsheetManager.fetch_allData(sheet)
    # headerとdataを分離する
    header = sheet_data[0]
    data = sheet_data[1:]
    df = pd.DataFrame(data,columns=header)
    
    # 出品中の商品情報の取得
    logger.info(f"出品情報取得開始")
    items = mercari.fetch_syuppin_item()
    
    update_items = []
    logger.info(f"更新用データ作成開始:{len(items)} 件")
    for item in items:
        # IDがタイトルもしくは説明文に含まれているか確認
        _row1 = contains_keywords_by_list(item.item_name, list(df['ID']))
        _row2 = contains_keywords_by_list(item.description, list(df['ID']))
        row = max(_row1, _row2)
        if row >= 0:
        #if len(df[df["タイトル"].str.contains(df['ID'])]) > 0 or len(df[df["説明文"].str.contains(df['ID'])]) > 0:
            # 存在するレコードの行番号を指定してUpdate
            logger.info(f"IDが存在するため、既存レコードを更新:{item.item_name}")
            _item_dict = _create_update_item_dict(item)
            spreadsheetManager.bulk_update_row2(sheet, [_item_dict], row+1)
            continue
        
        update_items.append(_create_update_item_dict(item))
    
    # スプレッドシートへ更新
    last_row = spreadsheetManager.get_last_row(sheet)
    logger.info(f"スプレッドシート更新開始:{len(items)} 件 / 最終行:{last_row}")
    spreadsheetManager.bulk_update_row2(sheet, update_items, last_row+1)
    logger.info("スプレッドシート更新完了")
    
    # 出品ステータス更新
    try:
        #update_syuppin_stat()
        # eelに通知
        eel.popup_alert(f"出品中のデータ取得が完了しました:{len(items)} 件")
    except Exception as e:
        logger.error(f"出品ステータス更新エラー:{e}")
        eel.popup_alert(f"出品ステータス更新エラー:{e}")


def _create_update_item_dict(item):
    # スプレッドシート更新用にデータ変換
    update_item_dict = {
        "タイトル": item.item_name,
        "説明文": item.description,
        "出品ID": item.item_id,
        "ブランド1": item.brand,
        "メルカリ商品状態": item.condition,
        "現在価格": int(item.price) # スプレッドシートに数値として認識させる
    }
    
    # カテゴリを分解してセット
    for i,category in enumerate(item.categories):
        update_item_dict[f"カテゴリ{i+1}"] = category
    
    return update_item_dict
    
@eel.expose
def update_syuppin_stat():
    sheet_id = load_spreadsheet()
    sheet = spreadsheetManager.connect_to_sheetname(sheet_id, "data")
    sheet_data = spreadsheetManager.fetch_allData(sheet)
    # headerとdataを分離する
    header = sheet_data[0]
    data = sheet_data[1:]
    df = pd.DataFrame(data,columns=header)
    
    # 商品ステータスの取得
    syuppin_stats,prices = mercari.fetch_syuppin_stat(list(df["出品ID"]))
    update_items = [{"出品": f'=hyperlink("{mercari.MYPAGE_ITEM_URL}/{item_id}","{syuppin_stat}")',
                    "現在価格": int(price) if price != '' else ""} for syuppin_stat,price,item_id in zip(syuppin_stats,prices,list(df["出品ID"]))]

    # スプレッドシートへ更新
    spreadsheetManager.bulk_update_row2(sheet, update_items, 2) # ヘッダを除く2行目からデータUpdate

def contains_keywords_by_list(target:str, keywords:list):
    '''
    targetにkeywordsが含まれているか(部分一致)チェックして、マッチした場合はindex番号を返す
    '''
    for i,keyword in enumerate(keywords):
        if keyword == '':
            continue
        if target.find(keyword) >= 0:
            print(i,keyword)
            return i + 1 # 行番号はindex+1
        
    return -1


if __name__ == "__main__":
    desktop.start(app_name,end_point,size)
