from sys import argv

def dist(a, b):
    d = 0
    for i in range(len(a)):
        if a[i] != b[i]: d += 1
    return d

def dists(words):
    nwords = len(words)
    l = len(words[0])
    ds = [[[] for j in range(l)] for i in range(nwords)]
    for i in range(nwords):
        ds[i]
        for j in range(i+1, nwords):
            d = dist(words[i], words[j])
            ds[i][d-1].append(j)
            ds[j][d-1].append(i)
    return ds

def best(nwords, l, ds):
    b, c = None, nwords
    for i in range(nwords):
        q = 0
        for j in range(l):
            q = max(q, len(ds[i][j]))
        if q < c:
            c = q
            b = i
    return b, c

def run(words):
    l = len(words[0])
    while True:
        ds = dists(words)
        b, c = best(len(words), l, ds)
        d = int(input('%s %d> ' % (words[b], c)))
        if d == 0:
            break
        words = [words[i] for i in ds[b][d-1]]

if len(argv) < 2:
    print("usage python fo.py <wordfile>")
    exit()
file = open('words.txt')
lines = file.readlines()
words = list(map(lambda line: line.strip(), lines))
run(words)