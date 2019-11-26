import pandas as pd
from collections import Counter
import imp
import sys
import os
import re


elsa = pd.read_excel('Processed Mintel database.xlsx')

issues=[]
[issues.extend(e.split(',')) for e in elsa.Issues]
issues=set(issues)
issues_insert='INSERT INTO `issues`(`name`) VALUES(\'{name}\');\n'
output=[issues_insert.format(name=i.strip()) for i in issues if i!='-']
with open(os.getcwd()+'\\issues.txt', 'wt') as f:
        f.write(''.join(output))

ingredients=[]
[ingredients.extend(e.split(',')) for e in elsa.Ingredients]
ingredients=set(ingredients)
ingredients_insert='INSERT INTO `ingredient_alpha`(`name`) VALUES(\'{name}\');\n'
output=[ingredients_insert.format(name=i.strip()) for i in ingredients if i!='-']
with open(os.getcwd()+'\\ingredients.txt', 'wt') as f:
        f.write(''.join(output))

claims=[]
[claims.extend(e.split(',')) for e in elsa.Claims]
claims=set(claims)
claims_insert='INSERT INTO `claims`(`name`) VALUES(\'{name}\');\n'
output=[claims_insert.format(name=i.strip()) for i in claims if i!='-']
with open(os.getcwd()+'\\claims.txt', 'wt') as f:
        f.write(''.join(output))

# find issues
claims=[]
[claims.append((idx,val)) for idx,val in enumerate(elsa.Claims) if type(val)==float]



def sanitize_value(val):
    return re.sub(r'\'','\\\'',val)
prod_inserts='INSERT INTO `project_elsa`.`product_alpha`(`id`,`product`,`type`,`brand`,`package_size`,`unit`,`price`,`image_url`,`desc`) VALUES(\'{id}\',\'{product}\',\'{type}\',\'{brand}\',{pksize},\'{unit}\',{price},\'{image_url}\',\'{desc}\');\n'
output=''
for i in elsa.index:
    output+=prod_inserts.format(id=elsa['Record ID'][i],type=elsa['Type'][i],brand=elsa['Brand'][i],product=elsa['Product'][i],pksize=elsa['Unit Pack Size (ml/g)'][i],unit=elsa['Packaging Units'][i],price=elsa['Price in local currency'][i],image_url=elsa['Image'][i],desc=elsa['Description'][i])
with open(os.getcwd()+'\\product.txt', 'wt') as f:
        f.write(''.join(output))