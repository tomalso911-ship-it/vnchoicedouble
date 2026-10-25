import io
p = 'training_manual.html'
s = io.open(p, encoding='utf-8').read()
bad = [
    '<div class="lbl l-zh" style="display:none"></div>',
    '<div class="lbl l-en" style="display:none"></div>',
]
tot = 0
for b in bad:
    tot += s.count(b)
    s = s.replace(b, '')
io.open(p, 'w', encoding='utf-8').write(s)
print('removed', tot)
