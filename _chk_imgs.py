import re, os
h = open('training_manual.html', encoding='utf-8').read()
s = re.findall(r'src="training_shots/([^"]+)"', h)
refs = list(dict.fromkeys(s))
out = []
out.append('refs %d' % len(refs))
for f in refs:
    out.append(('OK ' if os.path.exists('training_shots/' + f) else 'MISS ') + f)
open('_chk_imgs.txt', 'w', encoding='utf-8').write('\n'.join(out))
