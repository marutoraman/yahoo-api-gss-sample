import csv

def write_csv_file(path, list):
    with open(path, mode='w', encoding="utf-8_sig") as file:
        writer = csv.writer(file)
        writer.writerow(list)

def read_csv_file(path):
    with open(path, mode='r', newline='', encoding="utf-8_sig") as file:
        reader = csv.reader(file)
        list = [row for row in reader]
        return list

# main処理
def main():
    print("main")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()