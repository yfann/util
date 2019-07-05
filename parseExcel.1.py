# read excel to generate sql 
import xlrd
import re
from enum import Enum
import datetime

class ColType(Enum):
     STR = 1
     INT = 2
     DATE = 3
     FLOA = 4

file=''
output_path = ''

def read_excel():
    wb=xlrd.open_workbook(filename=file)
    # sheet number
    sheet1=wb.sheet_by_index(0)
    # get header
    start_row=sheet1.row_values(1)
    i=1
    id=300
    while i<=91:
        row=sheet1.row_values(i)
        create_table(row[3],id)
        i=i+1
        id=id+1


def create_table(name,id):
    sql="REPLACE INTO `user_authentication` (`id`,`type`, `identify`, `credential`, `is_main`, `is_test`) VALUES ({id}, \'NORMAL\', \'{name}\', \'1\', 0, 1);\n".format(id=id,name=name)
    sql2="REPLACE INTO `user_profile` (`id`, `username`, `email`, `avatar`, `phone`, `create_date`, `role_id`, `gender`, `province`, `city`, `country`, `last_login_time`, `is_new`, `is_deleted`) VALUES ({id}, \'{name}\', \'\', NULL, NULL, \'{date}\', 0, 0, NULL, NULL, NULL, NULL, 1, 0);\n".format(id=id,name=name,date=datetime.datetime.now())
    sql3="REPLACE INTO `user_goal` (`user_id`, `goal_id`, `is_current`, `create_date`) VALUES ({id}, 1, 0, \'{date}\');\n".format(id=id,date=datetime.datetime.now())
    with open(output_path, 'a') as f:
        f.write(sql+sql2+sql3)


read_excel()