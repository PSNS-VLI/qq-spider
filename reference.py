import re

pattern = re.compile('[A-Z]{1}.*?–[0-9]+.', re.M)
pattern_2 = re.compile('.*?\n',re.M)
data = []
data_2 = []

with open('reference.txt', 'r', encoding='utf-8') as f:
    data = pattern.findall(f.read())
    print(data)
    
with open('reference-cn.txt', 'r', encoding='utf-8') as f:
    data_2 = pattern_2.findall(f.read())
    print(data_2)   
 
with open('referencce-re.txt', 'w', encoding='utf-8') as f:
    content = ''
    for index in range(len(data)):
        content += f'{data[index]}\n{data_2[index]}'
    f.write(content)
