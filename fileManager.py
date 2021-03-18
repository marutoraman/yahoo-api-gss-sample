import csv

def write_to_csv(path, list):
    with open(path, mode='w', encoding="utf-8_sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(list)

def read_csv(path):
    with open(path, mode='r', encoding="utf-8_sig", newline="") as file:
        reader = csv.reader(file)
        list = [row for row in reader]
        return list

def add_to_csv(path, array):
    print("input:", array)
    list_data = read_csv(path)
    print("before:", list_data)
    list_data.append(array)
    print("added:", list_data)
    write_to_csv(path, list_data)

# main処理
def main():
    print("main")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()