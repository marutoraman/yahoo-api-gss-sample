import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import time

from common.logger import set_logger
logger= set_logger(__name__)

class Gdrive():
    
    def __init__(self, folder_id:str):
            self.folder_id = folder_id
            gauth = GoogleAuth(settings_file=os.path.join(os.getcwd(),"settings.yaml"))
            gauth.LocalWebserverAuth()
            #gauth.CommandLineAuth()
            self.drive = GoogleDrive(gauth)
            # logger.error(f"GoogleDrive認証エラー:{e}")
       
        
    def upload_file(self,file_path:str):
        f=self.drive.CreateFile()
        f.SetContentFile(file_path)
        f.Upload()
        print(f)
        
    def upload_file2(self,file_path:str):
        f=self.drive.CreateFile({"title":"test2.txt"})
        f.SetContentString("test")
        f.Upload()
        print(f)
        
    def fetch_file(self,download_dir:str,filename:str):
        try:
            for file in self.drive.ListFile({'q': f'title contains "{filename}"'}).GetList():
                f = self.drive.CreateFile({'id': file["id"]})
                f.GetContentFile(os.path.join(download_dir, f['title']))
        except Exception as e:
            logger.error(f"GoogleDriveファイルダウンロードエラー:{e}")
            
        
    def download_file(self,download_dir:str,filename:str):
        file_list = self.drive.ListFile({'q': f"'{self.folder_id}' in parents and trashed=false"}).GetList()
                
        for file in file_list:
            if file.get("title").find(filename) >= 0:
                f = self.drive.CreateFile({'id':file.get("id")})
                f.GetContentFile(os.path.join(download_dir,file.get("title")))
                time.sleep(0.5)

