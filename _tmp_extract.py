import re
t=open('choice_lite.html',encoding='utf-8').read()
m=re.search(r'<template id="instGanttTpl">(.*?)</template>', t, re.S)
if not m: print('no tpl'); exit(1)
html=m.group(1).strip()
scripts=re.findall(r'<script>(.*?)</script>', html, re.S)
open('_g_syntax.js','w',encoding='utf-8').write('\n'.join(scripts))
print('ok',len(scripts),'scripts')
