
import os
import math
import random
import datetime

output_file='c:/doc/es_data.txt'
provinces=["北京","上海","天津","重庆","河北","山西","内蒙","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","广西","海南","四川","贵州","云南","西藏","陕西","甘肃","宁夏","青海","新疆","香港","澳门","台湾"]

def generateBulkES(beginDate,endDate):
    begin=datetime.datetime.strptime(beginDate, "%Y-%m-%d").date()
    end=datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    diff=end-begin
    result=''
    for d in range(0,diff.days):
        currentDay=begin+datetime.timedelta(days=d)
        for p in provinces:
            result+='{ \"index\": { \"_type\": \"_doc\" }}\n'
            result+="{{\"name\":\"{name}\",\"value\":{value},\"date\":\"{date}\"}}\n".format(name=p,value=math.floor(random.random()*10),date=currentDay.strftime("%Y-%m-%d"))
        with open(output_file,'at', encoding='utf8') as f:
            f.write(result)


os.remove(output_file)
generateBulkES('2019-07-12','2019-07-31')
print('finish!')