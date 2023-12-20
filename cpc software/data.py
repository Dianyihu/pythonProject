# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/12/21 
@time: 02:01
'''


from pandas import read_csv, read_excel, read_table

df_list = []
cols_list = []
cat_cols_list = []


def load_data(file):
    if file.endswith('.csv'):
        df = read_csv(file, header=0)
    elif file.endswith('.xlsx') or file.endswith('.XLSX'):
        df = read_excel(file, header=0)
    elif file.endswith('.txt'):
        df = read_table(file, header=0)

    return df


def init(files):
    for i in files:
        add_file(i)
    cal_cols()


def add_file(i):
    global df_list, cols_list, cat_cols_list

    df = load_data(i)
    cols_list.append(df.columns.to_list())
    cat_cols_list.append(df.select_dtypes(exclude=['float64']).columns.to_list())
    df_list.append(df)
    cal_cols()


def rmv_file(i_index):
    global df_list, cols_list, cat_cols_list

    cols_list.pop(i_index)
    cat_cols_list.pop(i_index)
    df_list.pop(i_index)
    cal_cols()


def cal_cols():
    global cols, cat_cols

    cols, cat_cols = [], []
    for i in range(len(cols_list)):
        cols = list(set(cols)|set(cols_list[i]))
        cat_cols = list(set(cat_cols)|set(cat_cols_list[i]))

