
import os
import math
import random
import datetime

output_file='c:/doc/es_data.txt'
provinces=["重庆市","天津市","澳門","广东省","广西壮族自治区","江苏省","浙江省","西藏自治区","黑龙江省","四川省"]

def generateBulkES(beginDate,endDate):
    begin=datetime.datetime.strptime(beginDate, "%Y-%m-%d").date()
    end=datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    diff=end-begin
    for d in range(0,diff.days):
        result=''
        currentDay=begin+datetime.timedelta(days=d)
        for p in provinces:
            result+='{ \"index\": { \"_type\": \"_doc\" }}\n'
            result+="{{\"name\":\"{name}\",\"value\":{value},\"date\":\"{date}\"}}\n".format(name=p,value=math.floor(random.random()*10),date=currentDay.strftime("%Y-%m-%d"))
        with open(output_file,'at', encoding='utf8') as f:
            f.write(result)


def generateJSON():
    result="["
    options=[-1,0,1]
    for i in range(1,34):
        result+='{{\"quizId\":{id},\"correctOption\":{option}}},\n'.format(id=i,option=random.choice(options))
    print(result+"]")

# os.remove(output_file)
# generateBulkES('2019-07-12','2019-07-31')
#print('finish!')
generateJSON()