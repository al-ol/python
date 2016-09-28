import os
import sys
import hashlib
from collections import defaultdict


def write_same(start_folder):
    di = walk(start_folder)
    for i in di:
        if len(di[i]) > 1:
            print (":".join(di[i]))


def walk(start_folder):
    di = defaultdict(list)
    for d, dirs, files in os.walk(start_folder):
        for f in files:
            if f[0] != '.' and f[0] != '~':
                s = os.path.abspath(os.path.join(d, f))
                if not os.path.islink(s):
                    di[my_hash(s)].append(s)
    return di


def my_hash(s):
    with open(s, "rb") as f:
        tmp = f.read(1024)
        hasher = hashlib.md5()
        while len(tmp) > 0:
            hasher.update(tmp)
            tmp = f.read(1024)
    return hasher.hexdigest()


write_same(sys.argv[1])

