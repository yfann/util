import csv

def parseCSVToSql(path_in,path_out,tableName):
    content='use `skincubator-wechat`;\n'
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
    return values[:-1]+');\n'

def isStr(val):
    if val=='NULL':
        return False
    if val.isdigit():
        return False    
    return True


def insertWithExist(path_in,path_out,tableName):
    content='use `skincubator-wechat`;\n'
    with open(path_in,encoding="utf8") as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        insert_head=getHeader(headers,tableName)
        for row in f_csv:
            content+=insert_head+getValuesWithExists(row,tableName)
    with open(path_out, 'wt',encoding="utf8") as f:
        f.write(content)

def getValuesWithExists(row,tableName):
    values='SELECT '
    for v in row:
        if isStr(v):
            values+='\'{value}\','.format(value=v)
        else:
            values+='{value},'.format(value=v)
    return values[:-1]+' FROM dual WHERE NOT EXISTS(SELECT * FROM `{table}` WHERE id=\'{id}\');\n'.format(table=tableName,id=row[0])



def insertWithID(path_in,path_out,tableName,id):
    content='use `skincubator-wechat`;\n'
    with open(path_in,encoding="utf8") as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        insert_head=getHeaderWithID(headers,tableName)
        key_id=id
        for row in f_csv:
            content+=insert_head+getValuesWithID(row,key_id)
            key_id+=1
    with open(path_out, 'wt',encoding="utf8") as f:
        f.write(content)  

def getHeaderWithID(headers,tableName):
    insert='INSERT INTO `'+tableName+'`(id,'
    for head in headers:
        insert+='`{name}`,'.format(name=head)
    return insert[:-1]+') '

def getValuesWithID(row,id):
    values='VALUES({id},'.format(id=id)
    for v in row:
        if isStr(v):
            values+='\'{value}\','.format(value=v)
        else:
            values+='{value},'.format(value=v)
    return values[:-1]+');\n'    

# parseCSVToSql('C:\doc\skincubator\sql\question.csv','C:\doc\skincubator\sql\sql_question.sql','question_result')
# parseCSVToSql('C:\doc\skincubator\sql\quiz.csv','C:\doc\skincubator\sql\sql_quiz.sql','quiz_result')
# parseCSVToSql('C:\doc\skincubator\sql\\report.csv','C:\doc\skincubator\sql\sql_report.sql','report')
# parseCSVToSql('C:\doc\skincubator\sql\selfie.csv','C:\doc\skincubator\sql\sql_selfie.sql','selfie_result')
# insertWithExist('C:\doc\skincubator\sql\skin_user.csv','C:\doc\skincubator\sql\sql_user.sql','user')

#insertWithID('C:\doc\skincubator\sql\skin_question.csv','C:\doc\skincubator\sql\sql_skin_question.sql','skin_question',1500)
insertWithID('C:\doc\skincubator\sql\\recommend_product.csv','C:\doc\skincubator\sql\sql_recommend_product.sql','recommend_product',2050)