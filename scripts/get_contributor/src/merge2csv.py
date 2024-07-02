import glob
import pandas as pd


def get_file_list(path):
    return glob.glob(path)

# 遍历output文件夹下的所有csv文件


def csv2sheet():
    writer = pd.ExcelWriter('./output.xlsx')
    all_files = get_file_list('./output/*.csv')
    for filename in all_files:
        # 如果csv只有一行就不写入
        if len(open(filename, 'r').readlines()) == 1:
            continue

        pd.read_csv(filename).to_excel(writer, sheet_name=filename[9:-4], index=False)
    writer.close()


# csv2sheet()
