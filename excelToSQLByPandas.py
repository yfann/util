import pandas as pd
from collections import Counter
import imp
import sys
import os


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