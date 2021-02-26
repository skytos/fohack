from sys import argv

def same(a, b):
    c = 0
    for i in range(len(a)):
        if a[i] == b[i]: c += 1
    return c

def same_classes(words):
    l = len(words)
    wl = len(words[0])
    sc = [{} for i in range(l)]
    for i in range(len(words)):
        sc[i][wl] = set((i,))
        for j in range(i+1, len(words)):
            s = same(words[i], words[j])
            if s in sc[i]:
                sc[i][s].add(j)
            else:
                sc[i][s] = set((j,))
            if s in sc[j]:
                sc[j][s].add(i)
            else:
                sc[j][s] = set((i,))
    return sc

def decision_tree(same_classes, kill_depth=5):
    def rec(possible, depth):
        if depth >= kill_depth:
            return kill_depth, None
        if len(possible) == 1:
            return depth+1, {'guess': list(possible)[0], 'tree': None}
        
        best_depth = kill_depth
        best_tree = None
        for i in possible:
            sc = same_classes[i]
            max_depth = 0
            tree = {'guess': i, 'tree': {}}
            for s in sc:
                next_possible = possible.intersection(sc[s])
                if len(next_possible) > 0:
                    sub_depth, sub_tree = rec(next_possible, depth+1)
                    max_depth = max(max_depth, sub_depth)
                    if max_depth >= kill_depth:
                        break
                    tree['tree'][s] = sub_tree
            if max_depth < best_depth:
                best_depth = max_depth
                best_tree = tree
        return best_depth, best_tree
    
    return rec(set(range(len(same_classes))), 0)
    
def run(words):
    sc = same_classes(words)
    dt = decision_tree(sc)
    print(dt)

def main():
    if len(argv) < 2:
        print("usage python fo.py <wordfile>")
        exit()
    file = open('words.txt')
    lines = file.readlines()
    words = list(map(lambda line: line.strip(), lines))
    run(words)

if __name__ == '__main__':
    main()