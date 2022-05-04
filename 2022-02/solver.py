from docplex.mp.model import Model
import pandas as pd

def find_path(words, to_word = 'TIGER', num_guesses = 7, html_output = False):
    print(words)
    guesses = list(range(num_guesses))
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    positions = [0,1,2,3,4]
    occurences = {a: to_word.count(a) for a in alphabet}
    
    m = Model()
    
    x = {(g,p,a): m.binary_var() for g in guesses for a in alphabet for p in positions}
    word = {(g,w): m.binary_var() for g in guesses for w in words}
    min_occurrences = {(g,a): m.continuous_var() for g in guesses for a in alphabet}
    max_occurrences = {(g,a): m.continuous_var() for g in guesses for a in alphabet}
    
    # Basic constraint
    for g in guesses:
        m.add(m.sum(word[g,w] for w in words) == 1)
        for p in positions:
            m.add(m.sum(x[(g,p,a)] for a in alphabet) == 1)
        for w in words:
            for p in positions:
                m.add(word[(g,w)] <= x[(g,p,w[p])])
                
    # Last word = to_word
    m.add(word[(num_guesses-1, to_word)] == 1)
    for p in positions:
        m.add(x[(num_guesses-1, p, to_word[p])] == 1)
        
    # If a position was guessed correctly in the previous guess, it has to be correct in the next guess
    for g in guesses[:-1]:
        for p in positions:
            m.add(x[(g,p,to_word[p])] <= x[(g+1,p,to_word[p])])
            
    # If a letter was guessed correctly, but it doesn't occur in the guessed position, the letter is taboo in that position for the following guesses
    for g in guesses:
        for w in words:
            for p in positions:
                if w[p] in to_word and w[p] !=  to_word[p]:
                    for gg in guesses[g+1:]:
                        m.add(x[(gg,p,w[p])] <= 1-word[(g,w)])
            
    # Set min and max occurrences for each letter for the next guess
    for g in guesses[:-1]:
        for a in alphabet:
            m.add(min_occurrences[(g+1,a)] >= min_occurrences[(g,a)])
            m.add(max_occurrences[(g+1,a)] <= max_occurrences[(g,a)])
            mino = m.continuous_var()
        for w in words:
            for a in w:
                if w.count(a) > to_word.count(a):
                    m.add(min_occurrences[(g+1,a)] >= to_word.count(a)*word[(g,w)])
                    m.add(max_occurrences[(g+1,a)] <= 5*(1-word[(g,w)])+to_word.count(a))
                if w.count(a) <= to_word.count(a):
                    m.add(min_occurrences[(g+1,a)] >= w.count(a)*word[(g,w)])
                    
    for g in guesses[1:]:
        for a in alphabet:
            m.add(m.sum(x[(g,p,a)] for p in positions) >= min_occurrences[(g,a)])
            m.add(m.sum(x[(g,p,a)] for p in positions) <= max_occurrences[(g,a)])
                    
    # Words can't repeat:
    # for w in words:
#         m.add(m.sum(word[(g,w)] for g in guesses) <= 1)
        
    # Words can't repeat - objective formulation
    maxx = m.continuous_var()
    for w in words:
        m.add(m.sum(word[(g,w)] for g in guesses) <= maxx)
    m.minimize(maxx)
    
        
    m.solve(log_output = True)
    
    for g in guesses:
        for w in words:
            if word[(g,w)].solution_value > 0.5:
                print(w)
                
    if html_output:
        with open('output.html','w') as f:
            f.write('<pre>')
            for g in guesses:
                for w in words:
                    if word[(g,w)].solution_value > 0.5:
                        line = ''
                        incorrect_guesses = {a:to_word.count(a) for a in alphabet}
                        counter = 0
                        for a in w:
                            if a == to_word[counter]:
                                incorrect_guesses[a] -= 1
                            counter += 1
                        counter = 0
                        for a in w:
                            if a not in to_word:
                                line+=a
                            elif a == to_word[counter]:
                                line+='<span style="background-color:green">'+a+'</span>'
                            else:
                                if incorrect_guesses[a] > 0:
                                    line+='<span style="background-color:yellow">'+a+'</span>'
                                    incorrect_guesses[a] -= 1
                                else:
                                    line+=a
                            counter += 1
                f.write(line+'<br>')
            f.write('</bre>')
    
def get_words(file = 'words.csv'):
    words = []
    with open(file, 'r') as f:
        df = f.readlines()
        for line in df:
            words.append(line.strip())
    return words
    
words = get_words()
find_path(words, 'TIGER', num_guesses = 13, html_output = True)