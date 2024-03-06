def build_transition_table(pattern):
    m = len(pattern)
    alphabet = sorted(set(pattern), key=pattern.index)  
    transitions = []

  
    header = ["S"] + list(alphabet) + ["P(prefix)", "prefix + alfa"]
    transitions.append(header)

    for q in range(m + 1):
        row = [q]
        for char in alphabet:
            k = min(m + 1, q + 2)
            prefix_sufix = pattern[:q] + char

            max_attempts = m  
            while k > 0 and pattern[:q] + char != pattern[:k-1] and max_attempts > 0:
                k -= 1
                max_attempts -= 1

            row.append(k - 1)

        prefix = pattern[:q]
        alpha = ', '.join([prefix + char for char in alphabet])

    
        for i, char in enumerate(alphabet):
            if row[i + 1] == -1:
                i_unknown = pattern.rfind(char, 0, q)
                max_attempts = m  
                i_temp = q
                while i_temp > 0 and not pattern[:i_temp] == pattern[q-i_temp:q] and max_attempts > 0:
                    i_temp -= 1
                    max_attempts -= 1
                row[i + 1] = i_temp if pattern[:i_temp] == pattern[q-i_temp:q] else 0

        row += [prefix, alpha]
        transitions.append(row)

    return transitions





def sufix(sablon, k, q, a):
    prefix_sufix = sablon[:q] + a

    lengthP = k ## lungimea curenta a sablonului in procesul de verificare
    lengthS = q + 1 ## pozitia curenta in sirul prefix_sufix

    while lengthP > 0 and lengthS <= q + 1:
        if sablon[:lengthP] == prefix_sufix[lengthS - lengthP:]:  
            return True

        lengthP -= 1
        lengthS += 1

    return False



def computeTF(pat, M):
    global NR_DE_CARACTERE
    TF = [[0 for _ in range(NR_DE_CARACTERE)] for _ in range(M + 1)] ## matrice de dimensiuni (M+1) X NR_DE_CARACTERE (valori initializate cu 0)

    for state in range(M + 1): ## (parcurgem toate starile automatului)
        for x in range(NR_DE_CARACTERE): ## (parcurgem prin toate caracterele posibile)
            z = getNextState(pat, M, state, x) ## ne folosim de functia getNextState pentru a obtine urmatoarea stare 'z' a AF si caracterul 'x'
            TF[state][x] = z

    return TF


def search(pat, txt):
    
    global NR_DE_CARACTERE
    M = len(pat)
    N = len(txt)
    TF = computeTF(pat, M)    
 
    state = 0
    indices = []

    for i in range(N):
        state = TF[state][ord(txt[i])] ## obtinem urmatoarea stare a AF pt starea curenta si caracterul curent din text
        if state == M:
            indices.append(i - M + 1) ## indicele unde s-a gasit sablonul in lista.

    return indices

NR_DE_CARACTERE = 256

def getNextState(pat, M, state, x):
   
    if state < M and x == ord(pat[state]): ## daca starea este mai mica decat lungimea sablonului si daca 'x' este egal cu caracterul de pe pozitia curenta din sablonul dat.
        return state+1
    i=0
    for ns in range(state,0,-1):
        if ord(pat[ns-1]) == x:
            while(i<ns-1):
                if pat[i] != pat[state-ns+1+i]: ## verifica daca caracterele din sablon nu sunt identice
                    break
                i+=1
            if i == ns-1: 
                return ns ## locul unde a fost gasit un sufix care coincide cu un prefix.
    return 0

def print_transition_table_formatted(transitions):
    header = ["S"] + list(set(transitions[0][1:-2])) + ["P(prefix)", "prefix + alfa"]
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*transitions)]


    formatted_header = "|".join(f"{col.ljust(col_width)}" for col, col_width in zip(header, col_widths))
    print(formatted_header)
    print('-' * (sum(col_widths) + len(col_widths) - 1))

    for i, row in enumerate(transitions):
        if i == 1:
            continue  

        row_data = row[:-2]  
        row_data += [row[-2].replace('|', ',').replace(' ', ''), row[-1]]

        formatted_row = "|".join(f"{str(cell).ljust(col_width)}" for cell, col_width in zip(row_data, col_widths))
        print(formatted_row)

    print('-' * (sum(col_widths) + len(col_widths) - 1))


if __name__ == "__main__":
    pattern = input("Introdu patternul: ")
    transitions = build_transition_table(pattern)
    print_transition_table_formatted(transitions)