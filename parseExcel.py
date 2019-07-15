# read excel to generate sql 
import xlrd
import re
from enum import Enum

class ColType(Enum):
     STR = 1
     INT = 2
     DATE = 3
     FLOA = 4
     LONGSTR = 5

file='C:/doc/updated product database based on categories May 2019 v2.xlsx'
output_table='c:/doc/product_beta.txt'

def excel2Table():
    wb=xlrd.open_workbook(filename=file)
    # sheet number
    sheet1=wb.sheet_by_index(2)
    # get header
    header_row=sheet1.row_values(1)[:78]
    create_table(header_row,'product_beta')

def create_table(header_row,table_name=None):
    types=col_type(header_row)
    create_table_sql='CREATE TABLE `{name}` (\n'.format(name=table_name)
    for index,cell in enumerate(header_row):
        if index==0:
            create_table_sql+='`id` int(11) NOT NULL AUTO_INCREMENT,\n'
            continue
        create_table_sql+='`{name}`'.format(name=normalize_name(name_mapping(cell)))+sql_type_seg(types[index])
   
    create_table_sql+='PRIMARY KEY (`id`)\n) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8;'
    with open(output_table, 'wt') as f:
         f.write(create_table_sql)

def name_mapping(name):
    dic={'Unit Pack Size (ml/g)':'Unit Pack Size'}
    return dic.get(name,name)

def normalize_name(name):
    return re.sub(r'[\s+-/]','_',name.lower())

def sql_type_seg(type):
    str=''
    if ColType.STR==type:
        str=' varchar(100) DEFAULT NULL,\n'
    elif ColType.LONGSTR==type:
        str=' varchar(3000) DEFAULT NULL,\n'
    elif ColType.INT==type:
        str=' int(11) DEFAULT NULL,\n'
    elif ColType.DATE==type:
        str=' DATETIME DEFAULT NULL,\n'
    elif ColType.FLOA==type:
        str=' decimal(10,2) NULL,\n'
    return str


def col_type(header_row):
    def_col='str'
    int_cols=['Shampoo',  
   'sh_Oiliness',  
   'sh_Dandruff',  
   'sh_Damaged',  
   'sh_chemically treated',  
   'sh_Itchiness_sens_skindis',  
   'sh_Hair loss',  
   'sh_normal',  
   'sh_silicone free',  
   'sh_volume',  
   'Conditioner',  
   'Con_Hydration',  
   'Con_Long',  
   'Con_Softness',  
   'Con_Fly',  
   'Con_shine',  
   'Con_strength',  
   'Mask',  
   'mask_split_eds',  
   'mask_hydration',  
   'mask_strength',  
   'mask_shine',  
   'mask_softness',
   'Skin disorders',  
   'Sensitive',  
   'Dandruff',  
   'Itchiness',  
   'Oiliness',  
   'Hair loss',  
   'Damaged',  
   'Normal',  
   'Perm',  
   'color',  
   'Chemically treated',  
   'Silicone Free',  
   'Hydration',  
   'Long hair',  
   'Softness',  
   'Frizz',  
   'Fly-away',  
   'Shine',  
   'Strength',  
   'Strong',  
   'Split-ends',  
   'Volume',
   'Number of Variants']
    float_cols=['Unit Pack Size (ml/g)', 'Price in local currency']
    bigtext_cols=['Product Description',  'Primary Image Thumbnail', 'Record hyperlink','Remaining Ingredients' ]
    date_cols=[]
    types=[]
    for cell in header_row:
        if cell in int_cols:
            types.append(ColType.INT)
        elif cell in float_cols:
            types.append(ColType.FLOA)
        elif cell in date_cols:
            types.append(ColType.DATE)
        elif cell in bigtext_cols:
            types.append(ColType.LONGSTR)
        else:
            types.append(ColType.STR)
    return types

excel2Table()
print('process complete!')