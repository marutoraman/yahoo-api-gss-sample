from gdrive import *

def test_download_file():
    g = Gdrive("1qi-iyX9iOnV1XAHVtXFK0KUHvwqhp8GO")
    g.download_file("img","item-64")