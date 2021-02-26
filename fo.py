# takes 2 words and returns the number of characters that are the same
def same(a, b):
    c = 0
    for i in range(len(a)):
        if a[i] == b[i]: c += 1
    return c

# takes a list of words and returns a list mapping word index to a
# dictionary mapping same values to the set of other word indicies
# that have that same value
# so eg ['are', 'ate'] => [{2: set([1]), 3: set([0])}, {2: set([0]), 3: set([1])}]
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

# takes the results of same_classes above, the length of the words, and the
# maximum number of guesses
# returns the depth of the decision tree (total number of guesses required
# in the worst case) as well as the decision_tree
# the decision_tree is a dict with 2 keys 'guess' and 'tree'
# guess is the next word to guess, and tree is dict mapping same values
# to sub decision trees, when there are no more decisions to make 'tree' will
# be None
def decision_tree(same_classes, word_length, max_guesses):
    # recursive helper function that does the DFS
    # possible is the set of possible words, depth is how many guesses have
    # been made so far, and kill_depth stops the DFS when it gets that deep
    def rec(possible, depth, kill_depth):
        if depth >= kill_depth:
            # too deep, abort
            return kill_depth, None
        if len(possible) == 1:
            # you guessed it
            return depth+1, {'guess': list(possible)[0], 'tree': {word_length: None}}
        
        best_depth = kill_depth
        best_tree = None
        # loop over possible guesses
        for i in possible:
            sc = same_classes[i]
            max_depth = 0
            tree = {'guess': i, 'tree': {}}
            # for each same value fill in that value in the decision tree
            for s in sc:
                if s == word_length:
                    # you guessed it
                    tree['tree'][s] = None
                    continue
                next_possible = possible.intersection(sc[s])
                if len(next_possible) > 0:
                    # if there are possibilities for this same class recurse down that tree
                    sub_depth, sub_tree = rec(next_possible, depth+1, best_depth)
                    max_depth = max(max_depth, sub_depth)
                    if max_depth >= kill_depth:
                        # too deep, abort
                        break
                    tree['tree'][s] = sub_tree
            if max_depth < best_depth:
                best_depth = max_depth
                best_tree = tree
        return best_depth, best_tree
    
    all_words = set(range(len(same_classes)))
    return rec(all_words, 0, max_guesses + 1)

# run every possible answer word through the decision tree
def test(words, decision_tree):
    for answer in range(len(words)):
        print("answer %d" % answer)
        dt = decision_tree
        while dt:
            guess = dt['guess']
            s = same(words[answer], words[guess])
            print("guess: %d, same: %d" % (guess, s))
            dt = dt['tree'][s]
        print()

# make the decision tree and test it
def run(words):
    sc = same_classes(words)
    dd, dt = decision_tree(sc, len(words[0]), 4)
    print(dd, dt)
    test(words, dt)

# read words from "words.txt" and run against them
def main():
    file = open('words.txt')
    lines = file.readlines()
    words = list(map(lambda line: line.strip(), lines))
    run(words)

if __name__ == '__main__':
    main()