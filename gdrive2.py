import pprint
import google.oauth2.credentials
import os
 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
 
CLIENT_SECRETS_FILE = 'client_secrets.json' # 各自のclient_secret.jsonファイルへのパスを設定
SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
 
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
 
def list_drive_files(service, **kwargs):
  results = service.files().list(**kwargs).execute()
  pprint.pprint(results)
 
if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  service = get_authenticated_service()
  list_drive_files(service)