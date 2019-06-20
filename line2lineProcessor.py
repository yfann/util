import os
import json

input = 'C:/backup/aggregate_data_6_6.json'
output_path = 'C:/backup/'
output_file='output_'
page_size=100


def processFile(file):
    count=0
    output=""
    file_no=1
    for line in open(file,'r',encoding="utf8"):
        if count>=page_size or output=="":
            count=0
            output = os.path.join(output_path, output_file+str(file_no))
            file_no+=1
            with open(output, 'wt') as f:
                f.write('POST wechat_aggregate/_bulk\n')
        processLine(line,output)
        count+=1

def processLine(line,output):
    data=json.loads(line)
    with open(output, 'a') as f:
        f.write("{ \"index\": { \"_type\": \"wx\" }}"+'\n')
        f.write(json.dumps(data["_source"])+'\n')


processFile(input)

