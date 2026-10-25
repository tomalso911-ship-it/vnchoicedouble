path='c:/vnchoicedouble/choice_lite.html'
with open(path,'r',encoding='utf-8',errors='ignore') as f:
    text=f.read()
# Insert missing spaces using explicit Unicode escape for space (U+0020)
text=text.replace('Ngườitải', 'Ngườitải')
text=text.replace('Thờigian', 'Thờigian')
text=text.replace('ngườichỉ', 'ngườichỉ')
with open(path,'w',encoding='utf-8') as f:
    f.write(text)
print('done')
