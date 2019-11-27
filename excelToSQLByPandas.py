import pandas as pd
from collections import Counter
import imp
import sys
import os
import re
import math
elsa = pd.read_excel('Processed Mintel database.xlsx')
# insert issues
issues=[]
[issues.extend(e.split(',')) for e in elsa.Issues]
issues=[i.strip() for i in issues]
issues=set(issues)
issues_insert='INSERT INTO `issues`(`name`) VALUES(\'{name}\');\n'
output=[issues_insert.format(name=i) for i in issues if i!='-']
with open(os.getcwd()+'\\issues.txt', 'wt') as f:
        f.write(''.join(output))
# insert ingredients
ingredients=[]
[ingredients.extend(e.split(',')) for e in elsa.Ingredients]
ingredients=[i.strip() for i in ingredients]
ingredients=set(ingredients)
ingredients_insert='INSERT INTO `ingredient_alpha`(`name`) VALUES(\'{name}\');\n'
output=[ingredients_insert.format(name=i) for i in ingredients if i!='-']
with open(os.getcwd()+'\\ingredients.txt', 'wt') as f:
        f.write(''.join(output))
# insert claims
claims=[]
[claims.extend(e.split(',')) for e in elsa.Claims]
claims=[i.strip() for i in claims]
claims=set(claims)
claims_insert='INSERT INTO `claims`(`name`) VALUES(\'{name}\');\n'
output=[claims_insert.format(name=i) for i in claims if i!='-']
with open(os.getcwd()+'\\claims.txt', 'wt') as f:
        f.write(''.join(output))
# find issues for claims
claims=[]
[claims.append((idx,val)) for idx,val in enumerate(elsa.Claims) if type(val)==float]
# insert product
def sanitize_value(val):
    return re.sub(r'\'','\\\'',val)
def normalize_num(val):
    return 'null' if math.isnan(val) else val
prod_inserts='INSERT INTO `project_elsa`.`product_alpha`(`id`,`product`,`type`,`brand`,`package_size`,`unit`,`price`,`image_url`,`desc`) VALUES(\'{id}\',\'{product}\',\'{type}\',\'{brand}\',{pksize},\'{unit}\',{price},\'{image_url}\',\'{desc}\');\n'
output=''
for i in elsa.index:
    output+=prod_inserts.format(id=elsa['Record ID'][i],type=elsa['Type'][i],brand=sanitize_value(elsa['Brand'][i]),product=sanitize_value(elsa['Product'][i]),pksize=normalize_num(elsa['Unit Pack Size (ml/g)'][i]),unit=elsa['Packaging Units'][i],price=normalize_num(elsa['Price in local currency'][i]),image_url=elsa['Image'][i],desc=sanitize_value(elsa['Description'][i]))
with open(os.getcwd()+'\\product.txt', 'wt') as f:
    f.write(''.join(output))

# insert product-issues
template='insert into product_issues(product_id,issue_id) select {id},id from issues where `name`=\'{name}\';\n'
output=''
for i in elsa.index:
    if elsa.Issues[i]!='-':
        issues=elsa.Issues[i].split(',')
        for l in issues:
            output+=template.format(id=elsa['Record ID'][i],name=l.strip())
with open(os.getcwd()+'\\product_issues.txt', 'wt') as f:
    f.write(''.join(output))

# insert product-ingre
template='insert into product_ingredients(product_id,ingredient_id) select {id},id from ingredient_alpha where `name`=\'{name}\';\n'
output=''
for i in elsa.index:
    if elsa.Issues[i]!='-':
        issues=elsa.Ingredients[i].split(',')
        for l in issues:
            output+=template.format(id=elsa['Record ID'][i],name=l.strip())
with open(os.getcwd()+'\\product_ingredients.txt', 'wt') as f:
    f.write(''.join(output))