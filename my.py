import os
import sys
import hashlib
import os.path
from collections import defaultdict

di = defaultdict(list)
for d, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        if f[0] != '.' and f[0] != '~':
            s = d+'/' + f
            with open(s, "rb") as f:
                tmp = f.read(1024)
                hasher = hashlib.md5()
                while len(tmp) > 0:
                    hasher.update(tmp)
                    tmp = f.read(1024)
                di[hasher.hexdigest()].append(s)
for i, j in di.items():
    if (len(di[i]) > 1):
        print (":".join(j))

