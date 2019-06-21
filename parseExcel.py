# read excel to generate sql 
import xlrd
import re
from enum import Enum

class ColType(Enum):
     STR = 1
     INT = 2
     DATE = 3
     FLOA = 4

file='C:/doc/updated product database based on categories May 2019 v2.xlsx'
output=''

def read_excel():
    wb=xlrd.open_workbook(filename=file)
    # sheet number
    sheet1=wb.sheet_by_index(0)
    # get header
    header_row=sheet1.row_values(5)
    create_table(header_row,'product')

def create_table(header_row,table_name=None):
    types=col_type(header_row)
    create_table_sql='CREATE TABLE \'{name}\' (\n'.format(name=table_name)
    for index,cell in header_row:
        if index==1:
            create_table_sql+='\'id\' int(11) NOT NULL AUTO_INCREMENT,\n'
            continue
        create_table_sql+='\'{name}\''.formate(name=normalize_name(cell))+sql_type_seg(types[index])

    create_table_sql+=') ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8;'


def normalize_name(name):
    return re.sub(r'\s+','_',name.lower())

def sql_type_seg(type):
    str=''
    if ColType.STR==type:
        str=' varchar(100) DEFAULT NULL,\n'
    elif ColType.INT==type:
        str=' int(11) DEFAULT NULL,\n'
    elif ColType.DATE==type:
        str=' DATETIME DEFAULT NULL,\n'
    elif ColType.FLOA==type:
        str=' decimal(10,2) NULL,\n'
    return str


def col_type(header_row):
    def_col='str'
    int_cols=['Shampoo','Sch_Oiliness','Sch_Dandruff','Sch_Damaged','Chemically treated','Sch_Itchiness_sens_skindis','Sch_Hair loss','Sch_normal','Sch_silicone free',
    'Sch_volume','Conditioner','Con_Hydration','Con_Long','Con_Softness','Con_Fly','Con_shine','Con_strength','Mask','mask_split_eds','mask_hydration','mask_strength',
    'mask_shine','mask_softness','Skin disorders','Sensitive','Dandruff','Itchiness','Oiliness','Hair loss','Damaged','Normal','Perm','color','Chemically treated','Silicone Free',
    'Hydration','Long hair','Softness','Frizz','Fly-away','Shine','Strength','Strong','Split-ends','Volume','Number of Variants']
    date_cols=['Date Published']
    float_cols=['Price in US Dollars','Price in Euros','Unit Pack Size (ml/g)','Price in local currency']
    types=[]
    for cell in header_row:
        if cell in int_cols:
            types.append(ColType.INT)
        elif cell in float_cols:
            types.append(ColType.FLOA)
        elif cell in date_cols:
            types.append(ColType.DATE)
        else:
            types.append(ColType.STR)
    return types

read_excel()