import os, glob
fs = [(os.path.getsize(f)/1024, os.path.basename(f)) for f in glob.glob(r'C:\vnchoicedouble\training_shots\tri\*.png')]
fs.sort()
print('count', len(fs))
tiny = [n for s,n in fs if s < 15]
print('tiny(<15KB, possible blank):', tiny)
print('min %.1fKB  max %.1fKB' % (min(s for s,_ in fs), max(s for s,_ in fs)))
