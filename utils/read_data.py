import json

from utils.get_path import get_data_dir

path = get_data_dir()


# with 语句可以确保在使用完资源后正确地释放资源，无论代码块是否发生异常
# 使用 with 语句可以有效地管理文件、网络连接、数据库连接等资源，在使用完毕后自动进行清理和释放。

def read_json_data():
    with open(path+r"\data.json", 'r', encoding='utf') as f:
        data = json.load(f)
        return data

if __name__ == '__main__':
    print(read_json_data()["test_login"])
