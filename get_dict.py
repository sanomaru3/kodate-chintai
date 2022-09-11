def get_list(filename):

    import csv

    list = []
    
    # csv 読込み
    csvfile = open(filename, 'r')
    datas = csv.reader(csvfile)

    for data in datas:
        list.append(data[0])

    return list

def get_dict():

    import os

    dict = {}

    # file name 取得
    dir = "./japan"
    files = os.listdir(dir)

    for file in files:
        rf = './japan/' + file

        # file名抽出
        ken = file.replace('.csv', '')

        # dict追加
        dict[ken] = get_list(rf)
    
    return dict

