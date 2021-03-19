import fileManager

LOG_FILE = "log.csv"
CURRENT_DATA_FILE = "current_data.csv"

def check_duplication(path, list):
    print(" ... going to check duplication")
    file_data = fileManager.read_csv(path)
    if list in file_data:
        return True
    else:
        return False

def record(data):
    fileManager.add_to_csv(CURRENT_DATA_FILE, data)

def take_log(log):
    fileManager.add_to_csv(LOG_FILE, log)

# main処理
def main():
    print("main")
    take_log(["2010", "upload", "kore"])
    take_log(["2011", "upload", "kore"])


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()