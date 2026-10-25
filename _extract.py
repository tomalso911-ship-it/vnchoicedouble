import io, sys
src = 'choice_lite.html'
a, b = 4800, 5010
lines = io.open(src, encoding='utf-8', errors='replace').read().split('\n')
out = []
for i in range(a - 1, min(b, len(lines))):
    s = lines[i]
    if len(s) > 400:
        s = s[:400] + ' ...[truncated len=%d]' % len(lines[i])
    out.append('%d: %s' % (i + 1, s))
io.open('_wl_extract.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('WROTE', len(out), 'lines')
