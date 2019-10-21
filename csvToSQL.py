import csv

def parseCSVToSql(path_in,path_out,tableName):
    content=''
    with open(path_in,encoding="utf8") as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        insert_head=getHeader(headers,tableName)
        for row in f_csv:
            content+=insert_head+getValues(row)
    with open(path_out, 'wt',encoding="utf8") as f:
        f.write(content)

def getHeader(headers,tableName):
    insert='INSERT INTO `'+tableName+'`('
    for head in headers:
        insert+='`{name}`,'.format(name=head)
    return insert[:-1]+') '

def getValues(row):
    values='VALUES('
    for v in row:
        if isStr(v):
            values+='\'{value}\','.format(value=v)
        else:
            values+='{value},'.format(value=v)
    return values[:-1]+')\n'

def isStr(val):
    if val=='NULL':
        return False
    if val.isdigit():
        return False    
    return True

parseCSVToSql('C:\Data\question_result.csv','C:\Data\question.sql','test')