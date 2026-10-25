import esprima, sys
with open('c:/vnchoicedouble/choice_lite.html','r',encoding='utf-8') as f:
    lines=f.readlines()
start=None
for i,l in enumerate(lines):
    if '生产管理子系统（现场工厂）' in l:
        start=i
        break
end=None
for j in range(start, len(lines)):
    if '</script>' in lines[j]:
        end=j
        break
print('block lines', start+1, '->', end)
block = ''.join(lines[start+1:end])
try:
    esprima.parseScript(block)
    print('PROD SCRIPT PARSE OK')
except Exception as e:
    print('PARSE ERROR:', e)
    sys.exit(1)
