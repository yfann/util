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

file='C:/doc/User names for user tests.xlsx'
del_user='c:/doc/del_user.txt'
internal_user='c:/doc/internal_user.txt'
salon_user='c:/doc/salon_user.txt'
pebble_user='c:/doc/pebble_user.txt'

def read_excel():
    wb=xlrd.open_workbook(filename=file)
    # sheet number
    #sheet1=wb.sheet_by_index(0)
    #delete_users(sheet1)
    create_users(wb.sheet_by_index(0),internal_user)
    create_users(wb.sheet_by_index(1),salon_user)
    create_users(wb.sheet_by_index(2),pebble_user)
        


def create_table(name,id):
    sql="REPLACE INTO `user_authentication` (`id`,`type`, `identify`, `credential`, `is_main`, `is_test`) VALUES ({id}, \'NORMAL\', \'{name}\', \'1\', 0, 1);\n".format(id=id,name=name)
    sql2="REPLACE INTO `user_profile` (`id`, `username`, `email`, `avatar`, `phone`, `create_date`, `role_id`, `gender`, `province`, `city`, `country`, `last_login_time`, `is_new`, `is_deleted`) VALUES ({id}, \'{name}\', \'\', NULL, NULL, \'{date}\', 0, 0, NULL, NULL, NULL, NULL, 1, 0);\n".format(id=id,name=name,date=datetime.datetime.now())
    sql3="REPLACE INTO `user_goal` (`user_id`, `goal_id`, `is_current`, `create_date`) VALUES ({id}, 1, 0, \'{date}\');\n".format(id=id,date=datetime.datetime.now())
    with open(output_path, 'a') as f:
        f.write(sql+sql2+sql3)

def create_users(sheet,filename):
    start=1
    content=''
    for rownum in range(start, sheet.nrows):
        row=sheet.row_values(rownum) 
        content+=create_user_sql(row[4])
    with open(filename, 'wt') as f:
        f.write(content)

def create_user_sql(name):
    create_user="INSERT INTO `user_authentication` (`type`, `identify`, `credential`, `is_main`, `is_test`) VALUES (\'NORMAL\', \'{name}\', \'1\', 0, 1);\n".format(name=name)
    create_up="INSERT INTO `user_profile` (`id`, `username`, `email`, `avatar`, `phone`, `create_date`, `role_id`, `gender`, `province`, `city`, `country`, `last_login_time`, `is_new`, `is_deleted`) SELECT id, \'{name}\', \'\', NULL, NULL, \'{date}\', 0, 0, NULL, NULL, NULL, NULL, 1, 0 FROM `user_authentication` WHERE `identify`=\'{name}\';\n".format(name=name,date=datetime.datetime.now())
    create_ug="INSERT INTO `user_goal` (`user_id`, `goal_id`, `is_current`, `create_date`) SELECT id, 1, 0, \'{date}\' FROM `user_authentication` WHERE `identify`=\'{name}\';\n".format(name=name,date=datetime.datetime.now())  
    return create_user+create_up+create_ug

def delete_users(sheet):
    start=1
    safe='SET SQL_SAFE_UPDATES = 0;\n'
    content=''
    for rownum in range(start, sheet.nrows):
        row=sheet.row_values(rownum) 
        content+=delete_users_sql(row[3])
    with open(del_user, 'wt') as f:
        f.write(safe+content)

def delete_users_sql(name):
    del_up="DELETE FROM `user_profile` WHERE id IN (SELECT * FROM (SELECT id FROM `user_authentication` WHERE identify=\'{name}\') AS p);\n".format(name=name)
    del_g="DELETE FROM `user_goal` WHERE id IN (SELECT * FROM (SELECT id FROM `user_authentication` WHERE identify=\'{name}\') AS p);\n".format(name=name)
    del_users="DELETE FROM `user_authentication` WHERE identify=\'{name}\';\n".format(name=name)
    return del_up+del_g+del_users

read_excel()
print('finished!')